from ..repositories.users import UserRepo
from ..database.sqlalchemy.uow import UnitOfWork
from ..utils.abstract.unit_of_work import RepositoryDescriptor


class UserUOW(UnitOfWork):
    """
    A Unit of Work implementation that provides access to the User repository.

    Extends the base UnitOfWork and initializes the User repository.
    """

    users: UserRepo = RepositoryDescriptor(UserRepo)
