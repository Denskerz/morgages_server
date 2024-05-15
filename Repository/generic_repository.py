from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, List

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class GenericRepository(Generic[T], ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        raise NotImplementedError()

    @abstractmethod
    def list(self, **filters) -> List[T]:
        raise NotImplementedError()

    @abstractmethod
    def add(self, record: T) -> T:
        raise NotImplementedError()

    @abstractmethod
    def update(self, record: T) -> T:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, id: int) -> None:
        raise NotImplementedError()
