from types import TracebackType
from core.utils.abstract.repository import AbstractRepository
from database import new_session
from sqlalchemy.ext.asyncio import async_sessionmaker
from utils.abstract.unit_of_work import ABCUnitOfWork
from logging import getLogger
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any

logger = getLogger(__name__)


class UnitOfWork(ABCUnitOfWork):
    """
    Implementation of the Unit of Work pattern using SQLAlchemy's AsyncSession.

    Manages database sessions and transactions.
    """

    def __init__(self, sessionmaker: async_sessionmaker = new_session):
        """
        Initializes the UnitOfWork with a new session factory.
        """
        self.session_factory: async_sessionmaker = sessionmaker
        self.session: AsyncSession | None = None
        self._repositories: dict[str, Any] = {}

    def register_repository(self, name: str, repo: AbstractRepository) -> None:
        """
        Registers a repository in the UnitOfWork.
        """
        setattr(self, name, repo)
        self._repositories[name] = repo

    def __call__(self) -> "UnitOfWork":
        """
        Returns a new UnitOfWork instance with the same session factory.
        """
        return self.__class__(self.session_factory)

    async def __aenter__(self) -> "UnitOfWork":
        """
        Enters the asynchronous context and creates a new database session.

        Returns:
            UnitOfWork: The UnitOfWork instance.
        """
        for name, repo in self._repositories.items():
            self.register_repository(name, repo)
        logger.debug(f"Repositories: {self._repositories}")
        self.session = self.session_factory()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        Exits the asynchronous context, rolling back the transaction and closing the session.

        Args:
            *args: Arguments passed from the context manager.
        """
        for name in self._repositories.keys():
            delattr(self, name)
        self._repositories.clear()
        if exc_type is not None:
            logger.exception(
                f"Exception during {self.__class__.__name__} transcation execution",
                exc_info=(exc_type, exc_val, exc_tb),
            )
            await self.rollback()
        if self.session:
            await self.session.close()
        self.session = None

    async def commit(self, flush: bool = False) -> None:
        """
        Commits the transaction.

        Args:
            flush: Whether to flush the session before committing.
        """
        if self.session:
            if flush:
                await self.session.flush()
            await self.session.commit()

    async def rollback(self) -> None:
        """
        Rolls back the transaction.
        """
        if self.session:
            await self.session.rollback()
