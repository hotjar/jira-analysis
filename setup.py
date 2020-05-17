from os.path import abspath, dirname, join
from setuptools import setup

readme_file = join(dirname(abspath(__file__)), "README.md")


try:
    from m2r import parse_from_file

    readme = parse_from_file(readme_file)
except ImportError:
    with open(readme_file) as f:
        readme = f.read()

setup(
    author="Hotjar",
    author_email="scott.walton@hotjar.com",
    description="A set of tools for generating Jira reports",
    name="jira-analysis",
    install_requires=["arrow", "attrs", "bokeh", "click", "m2r", "requests", "toolz"],
    license="MIT",
    packages=["jira_analysis"],
    scripts=["bin/jira-analysis"],
    url="",
)
