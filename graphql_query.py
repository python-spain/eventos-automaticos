import httpx
import jwt
import os

from dotenv import load_dotenv

import logging
load_dotenv()

meetup_client_key = os.getenv("MEETUP_CLIENT_KEY")
meetup_client_secret = os.getenv("MEETUP_CLIENT_SECRET")
meetup_member_id = os.getenv("MEETUP_MEMBER_ID")


def auth():
    with httpx.Client(base_url="https://secure.meetup.com/oauth2/") as cli:
        data = {
            "sub": meetup_member_id,
            "iss": meetup_client_key,
            "aud": "api.meetup.com",
            "exp": 3600 * 4
        }
        logging.info(meetup_client_secret)
        logging.info(meetup_client_key)
        logging.info(meetup_member_id)
        signed_jwt = jwt.encode(data, meetup_client_secret, algorithm="RS256")
        r = cli.post(
            "/access",
            headers={
                "content-type": "application/x-www-form-urlencoded"
            },
            data={
                "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                "assertion": signed_jwt
            }
        )
        return r
