# Jira Ticket Analysis tools

A simple suite of tools that I use to graph 

## Setup instructions

```
git clone git@gitlab.com:hotjar/jira-analysis.git
python3 -m venv venv
. venv/bin/activation

pip install -r requirements.txt
```

You need to configure your Jira credentials and project config. This is two files:

* `credentials.yaml` for Jira credentials
* `config.yaml` for your project config

### `credentials.yaml`

```yaml
jira_credentials:
    email: your_email@example.com
    token: JIRA_TOKEN
```

### `config.yaml`

Use this to set your In Progress and Done statuses for each project you want to analyse. This lets you handle customised
workflows to get the right charts.

```yaml
projects:
  PROJECT_KEY:
    key: PROJECT_KEY
    in_progress:
      - In Progress
      - Review
    completed:
      - Done
```

## Running

```
./jira_analysis.py fetch <PROJECT_KEY> <tickets>.json
./jira_analysis analyse <PROJECT_KEY> <tickets>.json <chart>.html
```

## Why?

Jira is ridiculously customisable, to the point where it doesn't always easily support the reporting that you need in
the format that you have. Most of the time, people resolve this by dumping data into Excel and building custom charts
and reports.

The purpose of this is to work directly with Jira's API, which gives a lot more rich data, allowing us to get the
reports we want with minimal manual exporting, copying and pasting.

## License

[MIT](./LICENSE)
