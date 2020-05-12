#!/usr/bin/env python

import attr
import click
from typing import Iterable, Set

from analyse import print_cycle_times, average_cycle_times
from file_handlers import json
from update_tickets import load_from_file, persist_to_database, get_from_jira

from jira.issue import JiraTicket


@click.group()
def cli():
    click.echo("Starting")


@cli.command()
def load_from_jira():
    get_from_jira()


@cli.command()
@click.argument("project", type=str)
@click.option("-s", "source", type=click.Choice(["jira", "xml"]), default="jira")
@click.option("-o", "file_out", type=click.File("w"))
def fetch_tickets(project: str, source: str, file_out):
    """Fetch the tickets and save them as a JSON file.
    """
    tickets = get_from_jira(project.upper())
    json.dump([attr.asdict(ticket) for ticket in tickets], file_out)


@cli.command()
@click.argument("file_in", type=click.File())
def analyse(file_in):
    data = json.load(file_in)
    tickets = [JiraTicket.from_json(t) for t in data]
    print(tickets[0])


@cli.command()
@click.argument("project", type=str)
@click.option("-s", "source", type=click.Choice(["jira", "file"]), default="jira")
def analyse_tickets(project: str, source: str):
    """Analyse all tickets for a project.

    :param project: The project to analyse
    :param source: The source - either jira or file.
    """
    tickets = get_from_jira(project.upper())
    print_cycle_times(tickets)
    average_cycle_times(tickets)


@cli.command()
@click.argument("ticket_file", type=click.File())
def load(ticket_file):
    """Load tickets from the passed-in file.
    
    :param ticket_file: Path to the tickets to load (in XML format)
    """
    soup = load_from_file(ticket_file)
    persist_to_database(soup)


if __name__ == "__main__":
    cli()
