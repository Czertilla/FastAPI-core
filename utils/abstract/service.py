from typing import Generic, TypeVar
from utils.abstract.unit_of_work import ABCUnitOfWork


T = TypeVar("T", bound=ABCUnitOfWork)


class BaseService(Generic[T]):
    """
    Base service class for application services.

    Provides a common interface for services that require a Unit of Work.

    Attributes:
        uow (ABCUnitOfWork): The Unit of Work instance used by the service.
    """

    def __init__(self, uow: T) -> None:
        """
        Initializes the BaseService with a Unit of Work.

        Args:
            uow (ABCUnitOfWork): The Unit of Work instance.
        """
        self.uow: T = uow
