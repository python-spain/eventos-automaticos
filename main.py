#!/usr/bin/env python
"""
Publish meetup events to Telegram.
"""
import os

meetup_secret = os.environ["MEETUP_SECRET"]


def main():
    print(f"Hello Meetup! (secret {meetup_secret[:2]}{meetup_secret[2:] * '*'})")


if __name__ == '__main__':
    main()
