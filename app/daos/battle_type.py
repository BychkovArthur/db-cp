from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.daos.base import BaseDao
from app.models.user import BattleType


class BattleTypeDao(BaseDao):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create(self, battle_type: dict) -> BattleType:
        """Создать запись BattleType."""
        
        detailed_info_ = BattleType(**battle_type)
        self.session.add(detailed_info_)
        await self.session.commit()
        await self.session.refresh(detailed_info_)
        return detailed_info_

    async def get_by_id(self, detailed_info_id: int):
        return None
    #     """Получить запись UserDetailedInfo по ID."""
    #     statement = select(UserDetailedInfo).where(UserDetailedInfo.id == detailed_info_id)
    #     return await self.session.scalar(statement)

    async def get_all(self):
        return None
    #     """Получить все записи UserDetailedInfo."""
    #     statement = select(UserDetailedInfo).order_by(UserDetailedInfo.id)
    #     result = await self.session.execute(statement)
    #     return result.scalars().all()

    async def update_by_id(self, detailed_info_id: int, updated_data: dict):
        return None
    #     """Обновить запись UserDetailedInfo по ID."""
    #     statement = (
    #         update(UserDetailedInfo)
    #         .where(UserDetailedInfo.id == detailed_info_id)
    #         .values(**updated_data)
    #         .returning(UserDetailedInfo)
    #     )
    #     result = await self.session.execute(statement)
    #     await self.session.commit()
    #     return result.scalar_one_or_none()

    async def delete_all(self) -> None:
        return None
    #     """Удалить все записи UserDetailedInfo."""
    #     await self.session.execute(delete(UserDetailedInfo))
    #     await self.session.commit()

    async def delete_by_id(self, detailed_info_id: int):
        return None
    #     """Удалить запись UserDetailedInfo по ID."""
    #     detailed_info = await self.get_by_id(detailed_info_id)
    #     if detailed_info:
    #         await self.session.execute(delete(UserDetailedInfo).where(UserDetailedInfo.id == detailed_info_id))
    #         await self.session.commit()
    #     return detailed_info
