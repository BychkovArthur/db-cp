from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import Clan


class ClanDao:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, clan: dict) -> Clan:
        """Создать запись Clan."""
        query = text("""
            INSERT INTO clan (name, tag)
            VALUES (:name, :tag)
            RETURNING id, name, tag
        """)
        result = await self.session.execute(query, {"name": clan["name"], "tag": clan["tag"]})
        row = result.fetchone()
        return Clan(id=row.id, name=row.name)

    async def get_by_id(self, clan_id: int) -> Clan | None:
        """Получить запись Clan по ID."""
        query = text("""
            SELECT id, name
            FROM clan
            WHERE id = :id
        """)
        result = await self.session.execute(query, {"id": clan_id})
        row = result.fetchone()
        if row:
            return Clan(id=row.id, name=row.name)
        return None

    async def get_all(self) -> list[Clan]:
        """Получить все записи Clan."""
        query = text("""
            SELECT id, name
            FROM clan
            ORDER BY id
        """)
        result = await self.session.execute(query)
        rows = result.fetchall()
        return [Clan(id=row.id, name=row.name) for row in rows]

    async def update_by_id(self, clan_id: int, updated_data: dict) -> Clan | None:
        """Обновить запись Clan по ID."""
        query = text("""
            UPDATE clan
            SET name = :name
            WHERE id = :id
            RETURNING id, name
        """)
        result = await self.session.execute(query, {
            "id": clan_id,
            "name": updated_data["name"],
        })
        row = result.fetchone()
        await self.session.commit()
        if row:
            return Clan(id=row.id, name=row.name)
        return None

    async def delete_all(self) -> None:
        """Удалить все записи Clan."""
        query = text("""
            DELETE FROM clan
        """)
        await self.session.execute(query)
        await self.session.commit()

    async def delete_by_id(self, clan_id: int) -> Clan | None:
        """Удалить запись Clan по ID."""
        query = text("""
            DELETE FROM clan
            WHERE id = :id
            RETURNING id, name
        """)
        result = await self.session.execute(query, {"id": clan_id})
        row = result.fetchone()
        await self.session.commit()
        if row:
            return Clan(id=row.id, name=row.name)
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
            dao = ClanDao(session)

            new_clan = await dao.create({"name": "Warriors"})
            print("Created:", new_clan)

            clan = await dao.get_by_id(new_clan.id)
            print("Fetched by ID:", clan)

            all_clans = await dao.get_all()
            print("All clans:", all_clans)

            updated_clan = await dao.update_by_id(new_clan.id, {
                "name": "Elite Warriors",
            })
            print("Updated:", updated_clan)

            deleted_clan = await dao.delete_by_id(new_clan.id)
            print("Deleted:", deleted_clan)

            await dao.delete_all()
            print("All records deleted.")

    asyncio.run(main())
