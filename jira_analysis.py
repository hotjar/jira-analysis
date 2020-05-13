#!/usr/bin/env python

import attr
import click
from datetime import datetime

from analysis.ticket_control import generate_control_chart
from conversions.analysis import convert_jira_to_analysis
from file_handlers import json
from jira.issue import JiraTicket


@click.group()
def cli():
    click.echo("Starting")


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
@click.argument("file_out", type=str)
@click.option("date_start", "-s", type=click.DateTime())
def analyse(file_in, file_out, date_start: datetime):
    data = json.load(file_in)
    jira_tickets = [JiraTicket.from_json(t) for t in data]
    issues = (convert_jira_to_analysis(j) for j in jira_tickets)
    if date_start is not None:
        issues = (
            i
            for i in issues
            if i.completed is not None and i.completed.date() >= date_start.date()
        )
    generate_control_chart(list(issues), file_out)


if __name__ == "__main__":
    cli()
