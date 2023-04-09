#!/usr/bin/env python
"""
Publish meetup events to Telegram.
"""
import tomllib

meetup_client_secret = os.environ['MEETUP_SECRET']
meetup_client_key = os.environ['MEETUP_KEY']
meetup_member_id = os.environ['MEMBER_MEMBER_ID']


def get_events(community_slug):
    pass


def process_events():
    with open('communities.toml', 'rb') as f:
        for community in tomllib.load(f)['communities']:
            event = get_events(community)
            publish_to_telegram(event)


def publish_to_telegram(event):
    pass


def main():
    print(f"Hello Meetup! (secret {meetup_secret[:2]}{meetup_secret[2:] * '*'})")


if __name__ == '__main__':
    main()
