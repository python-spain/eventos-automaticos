import tomllib
from pprint import pprint

import click

from .graphql_query import collect_upcoming_events


@click.command()
@click.option(
    "--communities", "-c", "communities_path", type=click.Path(), required=True
)
def cli(communities_path):
    with open(communities_path, "rb") as f:
        communities_data = tomllib.load(f)
    communities = communities_data["communities"]

    upcoming_events = collect_upcoming_events(communities)
    pprint(upcoming_events)


if __name__ == "__main__":
    cli()
