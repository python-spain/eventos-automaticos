import httpx
import jwt
import datetime as dt
import os

from dotenv import load_dotenv

import logging

load_dotenv()

meetup_client_key = str(os.environ["MEETUP_CLIENT_KEY"])
meetup_client_secret = str(os.environ["MEETUP_CLIENT_SECRET"])
meetup_member_id = str(os.environ["MEETUP_MEMBER_ID"])
private_key = os.environ["MEETUP_JWT_KEY"].encode()


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
        return r
