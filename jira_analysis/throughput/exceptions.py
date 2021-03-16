class ThroughputException(Exception):
    """Base exception for throughput issues."""


class IssueNotComplete(ThroughputException):
    """Raised when an issue can't be created because it wasn't complete."""

    def __init__(self, key: str, status: str) -> None:
        super().__init__(f"Issue {key} is not completed. Status is {status}.")
