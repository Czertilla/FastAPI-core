from abc import ABC, abstractmethod
from typing import Any, Type, TypeVar

from .repository import AbstractRepository


T = TypeVar("T", bound=AbstractRepository)

class UOWMeta(type):
    def __new__(mcls, name, bases, namespace: dict[str, Any], **kwargs):
        repositories = {}
        for base in bases:
            if hasattr(base, '_repositories'):
                repositories.update(base._repositories)
        
        for k, v in namespace.items():
            if isinstance(v, RepositoryDescriptor):
                repositories[k] = v
        
        namespace['_repositories'] = repositories
        return super().__new__(mcls, name, bases, namespace)
    
class RepositoryDescriptor:
    def __init__(self, repo_type: Type):
        self.repo_type = repo_type
    
    def __set_name__(self, owner, name):
        self.name = name

class ABCUnitOfWork(ABC, metaclass=UOWMeta):
    """
    Abstract base class for Unit of Work implementations.

    Defines the interface for managing repositories and transactions.
    Supports variable number of repository types.
    """

    @abstractmethod
    def __init__(self):
        """
        Initializes the Unit of Work.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self) -> "ABCUnitOfWork":
        """
        Enters the asynchronous context.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args) -> None:
        """
        Exits the asynchronous context.

        Args:
            *args: Arguments passed from the context manager.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        """
        Commits the transaction.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        """
        Rolls back the transaction.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError
