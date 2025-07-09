from database import BaseRepo
from logging import getLogger

from ..models.user import UserORM as Model
from ..utils.abstract.repository import AbstractIdRepository

logger = getLogger(__name__)


class UserRepo(BaseRepo[Model], AbstractIdRepository):
    """
    Repository for managing UserORM entities.
    """

    model = Model

