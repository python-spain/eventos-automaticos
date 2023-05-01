import datetime as dt
import logging
import os

import httpx
import jwt
from dotenv import load_dotenv
from tenacity import retry
from tenacity.retry import retry_if_exception_type
from tenacity.stop import stop_after_attempt
from tenacity.wait import wait_exponential_jitter

load_dotenv()

meetup_client_key = str(os.environ["MEETUP_CLIENT_KEY"])
meetup_member_id = str(os.environ["MEETUP_MEMBER_ID"])
private_key = os.environ["MEETUP_JWT_KEY"].encode()


class MeetupAuthenticationError(RuntimeError):
    pass


class MeetupQueryError(RuntimeError):
    pass


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
        if not r.is_success:
            raise MeetupAuthenticationError(
                f"Could not perform authentication: {r.json()}"
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
        isNetworkEvent
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
    # TODO: There is supposedly a networkEvent subfield,
    # but it's completely undocumented

    with httpx.Client() as cli:
        response = cli.post(
            "https://api.meetup.com/gql",
            headers={
                "content_type": "application/json",
                "authorization": f"Bearer {token}",
            },
            json={"query": query, "variables": {"eventId": event_id}},
        )
        if not response.is_success:
            raise MeetupQueryError(f"{response.json()['errors']}")

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


def collect_upcoming_events(communities):
    token = auth()["access_token"]
    communities_upcoming_events = {}
    for community in communities:
        try:
            slug = community["slug"]
            url = community["url"]
            urlname = url.rstrip("/").split("/")[-1]
            upcoming_events = collect_group_upcoming_events(urlname, token)
            if upcoming_events:
                communities_upcoming_events[slug] = upcoming_events
        except Exception as e:
            logging.exception(
                f"Could not collect upcoming_events of community {url}", exc_info=e
            )
    return communities_upcoming_events
