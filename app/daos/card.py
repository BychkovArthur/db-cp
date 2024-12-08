from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import Card


class CardDao:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, card: dict) -> Card:
        """Создать запись Card."""
        query = text("""
            INSERT INTO card (name, type, level)
            VALUES (:name, :type, :level)
            RETURNING id, name, type, level
        """)
        result = await self.session.execute(query, {
            "name": card["name"],
            "type": card["type"],
            "level": card["level"],
        })
        row = result.fetchone()
        await self.session.commit()
        return Card(id=row.id, name=row.name, type=row.type, level=row.level)

    async def get_by_id(self, card_id: int) -> Card | None:
        """Получить запись Card по ID."""
        query = text("""
            SELECT id, name, type, level
            FROM card
            WHERE id = :id
        """)
        result = await self.session.execute(query, {"id": card_id})
        row = result.fetchone()
        if row:
            return Card(id=row.id, name=row.name, type=row.type, level=row.level)
        return None

    async def get_all(self) -> list[Card]:
        """Получить все записи Card."""
        query = text("""
            SELECT id, name, type, level
            FROM card
            ORDER BY id
        """)
        result = await self.session.execute(query)
        rows = result.fetchall()
        return [Card(id=row.id, name=row.name, type=row.type, level=row.level) for row in rows]

    async def update_by_id(self, card_id: int, updated_data: dict) -> Card | None:
        """Обновить запись Card по ID."""
        query = text("""
            UPDATE card
            SET name = :name, type = :type, level = :level
            WHERE id = :id
            RETURNING id, name, type, level
        """)
        result = await self.session.execute(query, {
            "id": card_id,
            "name": updated_data["name"],
            "type": updated_data["type"],
            "level": updated_data["level"],
        })
        row = result.fetchone()
        await self.session.commit()
        if row:
            return Card(id=row.id, name=row.name, type=row.type, level=row.level)
        return None

    async def delete_all(self) -> None:
        """Удалить все записи Card."""
        query = text("""
            DELETE FROM card
        """)
        await self.session.execute(query)
        await self.session.commit()

    async def delete_by_id(self, card_id: int) -> Card | None:
        """Удалить запись Card по ID."""
        query = text("""
            DELETE FROM card
            WHERE id = :id
            RETURNING id, name, type, level
        """)
        result = await self.session.execute(query, {"id": card_id})
        row = result.fetchone()
        await self.session.commit()
        if row:
            return Card(id=row.id, name=row.name, type=row.type, level=row.level)
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
            dao = CardDao(session)

            new_card = await dao.create({"name": "Archer", "type": "Troop", "level": 5})
            print("Created:", new_card)

            card = await dao.get_by_id(new_card.id)
            print("Fetched by ID:", card)

            all_cards = await dao.get_all()
            print("All cards:", all_cards)

            updated_card = await dao.update_by_id(new_card.id, {
                "name": "Archer Queen",
                "type": "Hero",
                "level": 10,
            })
            print("Updated:", updated_card)

            deleted_card = await dao.delete_by_id(new_card.id)
            print("Deleted:", deleted_card)

            await dao.delete_all()
            print("All records deleted.")

    asyncio.run(main())
