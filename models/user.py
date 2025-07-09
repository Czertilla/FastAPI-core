from sqlalchemy.orm import Mapped

from ..database.sqlalchemy.core import Base
from ..database.sqlalchemy.mixins.models import UUIDMixin


class UserORM(UUIDMixin, Base):
    """
    SQLAlchemy model representing a user.

    Attributes:
        id (UUID): The ID of the user, primary key.
        first_name (str | None): The first name of the user, can be None.
        last_name (str | None): The last name of the user, can be None.
        language_code (str | None): The language code of the user, can be None.
    """

    __tablename__ = "user"

    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    language_code: Mapped[str | None]