import json
import logging
import tomllib
from pathlib import Path

import click
import structlog
from dateutil.parser import parse as parse_date

from .graphql_query import collect_upcoming_events

logger = structlog.get_logger()


def event_name_from_data(event):
    event_start_time = parse_date(event["dateTime"])
    return (
        f"{event_start_time:%Y-%m-%d}_{event['title'].replace(' ', '-')}_{event['id']}"
    )


@click.command()
@click.option(
    "--communities", "-c", "communities_path", type=click.Path(), required=True
)
@click.option("--destination-dirname", "-d", type=click.Path(), default="_events")
@click.option("--verbose", "-v", is_flag=True)
def cli(communities_path, destination_dirname, verbose):
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.INFO if verbose else logging.WARNING
        ),
    )

    with open(communities_path, "rb") as f:
        communities_data = tomllib.load(f)
    communities = communities_data["communities"]

    upcoming_events = collect_upcoming_events(communities)

    if not (destination_dir := Path(destination_dirname)).is_dir():
        destination_dir.mkdir()

    for community_slug, events in upcoming_events.items():
        if not (community_dir := (destination_dir / community_slug)).is_dir():
            community_dir.mkdir()

        for event_data in events:
            event = event_data["data"]["event"]
            with open(community_dir / f"{event_name_from_data(event)}.json", "w") as fh:
                json.dump(event, fh, indent=2)


if __name__ == "__main__":
    cli()
