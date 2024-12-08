from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import BattleType


class BattleTypeDao:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, battle_type: dict) -> BattleType:
        """Создать запись BattleType."""
        query = text("""
            INSERT INTO battle_type (name)
            VALUES (:name)
            RETURNING id, name
        """)
        result = await self.session.execute(query, {"name": battle_type["name"]})
        row = result.fetchone()
        await self.session.commit()
        return BattleType(id=row.id, name=row.name)

    async def get_by_id(self, battle_type_id: int) -> BattleType | None:
        """Получить запись BattleType по ID."""
        query = text("""
            SELECT id, name
            FROM battle_type
            WHERE id = :id
        """)
        result = await self.session.execute(query, {"id": battle_type_id})
        row = result.fetchone()
        if row:
            return BattleType(id=row.id, name=row.name)
        return None


    async def get_all(self) -> list[BattleType]:
        """Получить все записи BattleType."""
        query = text("""
            SELECT id, name
            FROM battle_type
            ORDER BY id
        """)
        result = await self.session.execute(query)
        rows = result.fetchall()
        return [BattleType(id=row.id, name=row.name) for row in rows]

    async def update_by_id(self, battle_type_id: int, updated_data: dict) -> BattleType | None:
        """Обновить запись BattleType по ID."""
        query = text("""
            UPDATE battle_type
            SET name = :name
            WHERE id = :id
            RETURNING id, name
        """)
        result = await self.session.execute(query, {"id": battle_type_id, "name": updated_data["name"]})
        row = result.fetchone()
        await self.session.commit()
        if row:
            return BattleType(id=row.id, name=row.name)
        return None

    async def delete_all(self) -> None:
        """Удалить все записи BattleType."""
        query = text("""
            DELETE FROM battle_type
        """)
        await self.session.execute(query)
        await self.session.commit()

    async def delete_by_id(self, battle_type_id: int) -> BattleType | None:
        """Удалить запись BattleType по ID."""
        query = text("""
            DELETE FROM battle_type
            WHERE id = :id
            RETURNING id, name
        """)
        result = await self.session.execute(query, {"id": battle_type_id})
        row = result.fetchone()
        await self.session.commit()
        if row:
            return BattleType(id=row.id, name=row.name)
        return None


if __name__ == "__main__":
    import asyncio
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker

    async def main():
        DATABASE_URL = "postgresql+asyncpg://user:password@localhost/testdb"
        engine = create_async_engine(DATABASE_URL, echo=True)
        async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

        async with async_session() as session:
            dao = BattleTypeDao(session)

            # Пример создания записи
            new_battle_type = await dao.create({"name": "Epic Battle"})
            print("Created:", new_battle_type)

            # Пример получения по ID
            battle_type = await dao.get_by_id(new_battle_type.id)
            print("Fetched by ID:", battle_type)

            # Пример получения всех записей
            all_battle_types = await dao.get_all()
            print("All battle types:", all_battle_types)

            # Пример обновления записи
            updated_battle_type = await dao.update_by_id(new_battle_type.id, {"name": "Legendary Battle"})
            print("Updated:", updated_battle_type)

            # Пример удаления по ID
            deleted_battle_type = await dao.delete_by_id(new_battle_type.id)
            print("Deleted:", deleted_battle_type)

            # Пример удаления всех записей
            await dao.delete_all()
            print("All records deleted.")

    asyncio.run(main())
