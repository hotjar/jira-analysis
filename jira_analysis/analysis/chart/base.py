import attr

from abc import ABC, abstractmethod
from bokeh.models.sources import DataSource
from typing import Type


@attr.s
class BaseDataConverter(ABC):
    """Base drawing tools.
    """

    @abstractmethod
    def to_data_source(self, data_source: Type[DataSource]) -> DataSource:
        pass
