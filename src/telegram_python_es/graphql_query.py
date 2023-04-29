import tomllib
import httpx
import jwt
import datetime as dt
import os

from dotenv import load_dotenv
from tenacity import retry
from tenacity.stop import stop_after_attempt
from tenacity.wait import wait_exponential_jitter
from tenacity.retry import retry_if_exception_type

import logging

load_dotenv()

meetup_client_key = str(os.environ["MEETUP_CLIENT_KEY"])
meetup_member_id = str(os.environ["MEETUP_MEMBER_ID"])
private_key = os.environ["MEETUP_JWT_KEY"].encode()


@retry(
    stop=stop_after_attempt(10),
    wait=wait_exponential_jitter(initial=1, max=15, exp_base=2, jitter=0.2),
    retry=retry_if_exception_type(httpx.ConnectTimeout),
)
def auth():
    with httpx.Client(base_url="https://secure.meetup.com/oauth2/") as cli:
        # private_key = b"""-----BEGIN RSA PRIVATE KEY-----
        data = {
            "sub": meetup_member_id,
            "iss": meetup_client_key,
            "aud": "api.meetup.com",
            "exp": dt.datetime.utcnow() + dt.timedelta(seconds=120),
        }
        signed_jwt = jwt.encode(data, private_key, algorithm="RS256")
        r = cli.post(
            "/access",
            headers={"content-type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                "assertion": signed_jwt,
            },
        )
        return r.json()


def query_event(event_id: str, token: str):
    query = """
    query ($eventId: ID) {
      event(id: $eventId) {
        id
        title
        eventUrl
        description
        shortDescription
        group {
          id
          name
        }
        isOnline
        eventType
        venue {
          id
          name
          address
          city
          postalCode
          lng
          lat
        }
        onlineVenue {
          url
        }
        dateTime
        duration
        timezone
        endTime
      }
    }
    """
    with httpx.Client() as cli:
        response = cli.post(
            "https://api.meetup.com/gql",
            headers={
                "content_type": "application/json",
                "authorization": f"Bearer {token}",
            },
            json={"query": query, "variables": {"eventId": event_id}},
        )
        return response.json()


def query_group_events(urlname: str, token: str):
    query = """
    query ($urlname: String!) {
      groupByUrlname(urlname: $urlname) {
        urlname
        upcomingEvents(input: {}) {
          count
          edges {
            node {
              id
            }
            cursor
          }
        }
      }
    }"""
    with httpx.Client() as cli:
        response = cli.post(
            "https://api.meetup.com/gql",
            headers={
                "content_type": "application/json",
                "authorization": f"Bearer {token}",
            },
            json={"query": query, "variables": {"urlname": urlname}},
        )
        return response.json()


@retry(
    stop=stop_after_attempt(10),
    wait=wait_exponential_jitter(initial=1, max=15, exp_base=2, jitter=0.2),
    retry=retry_if_exception_type(httpx.ConnectTimeout),
)
def collect_group_upcoming_events(urlname: str, token: str):
    logging.info("Collecting upcoming events for group: %s", urlname)
    result = query_group_events(urlname=urlname, token=token)
    upcoming_events = result["data"]["groupByUrlname"]["upcomingEvents"]
    count = upcoming_events["count"]
    if count == 0:
        logging.info("There isn't any upcoming event for: %s", urlname)
        return {}
    events = [
        query_event(item["node"]["id"], token) for item in upcoming_events["edges"]
    ]
    logging.info("Collected upcoming events for group: %s", urlname)
    return events


def collect_upcoming_events():
    token = auth()["access_token"]
    with open("communities.toml") as f:
        data = tomllib.load(f)
    communities = data["communities"]
    communities_upcoming_events = {}
    for community in communities:
        try:
            url = community["url"]
            urlname = url.replace("https://www.meetup.com/", "").replace("/", "")
            upcoming_events = collect_group_upcoming_events(urlname, token)
            if upcoming_events:
                communities_upcoming_events[urlname] = upcoming_events
        except Exception as e:
            logging.exception(
                f"Could not collect upcoming_events of community {url}", exc_info=e
            )
    return communities_upcoming_events
