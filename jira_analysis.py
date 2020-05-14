#!/usr/bin/env python

import attr
import click
from datetime import datetime

from analysis.config import get_config as analysis_config
from analysis.ticket_control import generate_control_chart
from conversions.analysis import convert_jira_to_analysis
from file_handlers import json
from jira.auth import get_config as jira_config
from jira.issue import JiraTicket
from jira.network import get_issues, get_project


@click.group()
def cli():
    click.echo("Starting")


@cli.command()
@click.argument("project", type=str)
@click.argument("file_out", type=click.File("w"))
def fetch_tickets(project: str, file_out):
    """Fetch the tickets and save them as a JSON file.
    """
    config = jira_config("./credentials.yaml")
    tickets = get_issues(config, get_project(config, project.upper()))
    json.dump([attr.asdict(ticket) for ticket in tickets], file_out)


@cli.command()
@click.argument("project", type=str)
@click.argument("file_in", type=click.File())
@click.argument("file_out", type=str)
@click.option("date_start", "-s", type=click.DateTime())
def analyse(project, file_in, file_out, date_start: datetime):
    config = analysis_config(project, "./config.yaml")
    data = json.load(file_in)
    jira_tickets = [JiraTicket.from_json(t) for t in data]
    issues = (convert_jira_to_analysis(config, j) for j in jira_tickets)
    if date_start is not None:
        issues = (
            i
            for i in issues
            if i.completed is not None and i.completed.date() >= date_start.date()
        )
    generate_control_chart(list(issues), file_out)


if __name__ == "__main__":
    cli()
