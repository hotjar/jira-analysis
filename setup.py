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
    name="jira-analysis",
    description="A set of tools for generating Jira reports",
    url="",
    author="Hotjar",
    author_email="scott.walton@hotjar.com",
    license="MIT",
    packages=["jira_analysis"],
    install_requires=["arrow", "attrs", "bokeh", "click", "m2r", "requests", "toolz"],
)
