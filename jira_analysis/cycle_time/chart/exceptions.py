class ChartError(Exception):
    """Raised for any generic chart-related error."""


class NoTicketsProvided(ChartError):
    """Raised when no tickets are provided to generate a chart from."""

    def __init__(self) -> None:
        super().__init__(
            "No tickets provided. Check your local data was fetched correctly."
        )
