from abc import abstractmethod
from typing import Any, Generic
from sqlalchemy import Result, delete, exists, select, update

from ....utils.abstract.repository import AbstractIdRepository
from ..mixins.models import IDMixin as Model, ID


class IDRepositoryMixin(Generic[Model, ID], AbstractIdRepository):
    model: type[Model]

    @abstractmethod
    async def execute(self, stmt) -> Result:
        raise NotImplementedError

    async def _get_with_options(self, id: ID, options: tuple) -> Model | None:
        stmt = select(self.model).where(self.model.id == id).options(*options)
        return (await self.execute(stmt)).unique().scalar_one_or_none()

    async def get_by_id(self, id: ID, options: tuple = None) -> Model | None:
        if options:
            return await self._get_with_options(id, options)
        stmt = select(self.model).where(self.model.id == id)
        return (await self.execute(stmt)).scalar_one()

    async def update_one(self, id: ID, data: dict[str, Any]) -> Result:
        stmt = update(self.model).where(self.model.id == id).values(**data)
        return await self.execute(stmt)

    async def update_many(
        self, data: dict[str, dict[str, Any]], options: tuple = ()
    ) -> None:
        stmt = (
            update(self.model)
            .where(self.model.id.in_(data.keys()))
            .values(**data)
            .options(*options)
        )
        return await self.execute(stmt, flush=True)

    async def exists(self, id: ID) -> bool:
        return (
            await self.execute(select(exists().where(self.model.id == id)))
        ).scalar()

    async def delete_one(self, id: ID) -> None:
        await self.execute(delete(self.model).where(self.model.id == id))
