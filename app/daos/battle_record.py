from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import BattleRecord


class BattleRecordDao:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, battle_record: dict) -> BattleRecord:
        """Создать запись BattleRecord."""
        query = text("""
            INSERT INTO battle_record (subscribe_id, user1_score, user2_score, 
                                       user1_get_crowns, user2_get_crowns, 
                                       user1_card_ids, user2_card_ids, replay)
            VALUES (:subscribe_id, :user1_score, :user2_score, 
                    :user1_get_crowns, :user2_get_crowns, 
                    :user1_card_ids, :user2_card_ids, :replay)
            RETURNING id, subscribe_id, user1_score, user2_score, 
                      user1_get_crowns, user2_get_crowns, 
                      user1_card_ids, user2_card_ids, replay
        """)
        result = await self.session.execute(query, battle_record)
        row = result.fetchone()
        await self.session.commit()
        return BattleRecord(
            id=row.id,
            subscribe_id=row.subscribe_id,
            user1_score=row.user1_score,
            user2_score=row.user2_score,
            user1_get_crowns=row.user1_get_crowns,
            user2_get_crowns=row.user2_get_crowns,
            user1_card_ids=row.user1_card_ids,
            user2_card_ids=row.user2_card_ids,
            replay=row.replay
        )

    async def get_by_id(self, battle_record_id: int) -> BattleRecord | None:
        """Получить запись BattleRecord по ID."""
        query = text("""
            SELECT id, subscribe_id, user1_score, user2_score, 
                   user1_get_crowns, user2_get_crowns, 
                   user1_card_ids, user2_card_ids, replay
            FROM battle_record
            WHERE id = :id
        """)
        result = await self.session.execute(query, {"id": battle_record_id})
        row = result.fetchone()
        if row:
            return BattleRecord(
                id=row.id,
                subscribe_id=row.subscribe_id,
                user1_score=row.user1_score,
                user2_score=row.user2_score,
                user1_get_crowns=row.user1_get_crowns,
                user2_get_crowns=row.user2_get_crowns,
                user1_card_ids=row.user1_card_ids,
                user2_card_ids=row.user2_card_ids,
                replay=row.replay
            )
        return None

    async def get_all(self) -> list[BattleRecord]:
        """Получить все записи BattleRecord."""
        query = text("""
            SELECT id, subscribe_id, user1_score, user2_score, 
                   user1_get_crowns, user2_get_crowns, 
                   user1_card_ids, user2_card_ids, replay
            FROM battle_record
            ORDER BY id
        """)
        result = await self.session.execute(query)
        rows = result.fetchall()
        return [
            BattleRecord(
                id=row.id,
                subscribe_id=row.subscribe_id,
                user1_score=row.user1_score,
                user2_score=row.user2_score,
                user1_get_crowns=row.user1_get_crowns,
                user2_get_crowns=row.user2_get_crowns,
                user1_card_ids=row.user1_card_ids,
                user2_card_ids=row.user2_card_ids,
                replay=row.replay
            ) for row in rows
        ]

    async def update_by_id(self, battle_record_id: int, updated_data: dict) -> BattleRecord | None:
        """Обновить запись BattleRecord по ID."""
        query = text("""
            UPDATE battle_record
            SET subscribe_id = :subscribe_id,
                user1_score = :user1_score,
                user2_score = :user2_score,
                user1_get_crowns = :user1_get_crowns,
                user2_get_crowns = :user2_get_crowns,
                user1_card_ids = :user1_card_ids,
                user2_card_ids = :user2_card_ids,
                replay = :replay
            WHERE id = :id
            RETURNING id, subscribe_id, user1_score, user2_score, 
                      user1_get_crowns, user2_get_crowns, 
                      user1_card_ids, user2_card_ids, replay
        """)
        result = await self.session.execute(query, {**updated_data, "id": battle_record_id})
        row = result.fetchone()
        await self.session.commit()
        if row:
            return BattleRecord(
                id=row.id,
                subscribe_id=row.subscribe_id,
                user1_score=row.user1_score,
                user2_score=row.user2_score,
                user1_get_crowns=row.user1_get_crowns,
                user2_get_crowns=row.user2_get_crowns,
                user1_card_ids=row.user1_card_ids,
                user2_card_ids=row.user2_card_ids,
                replay=row.replay
            )
        return None

    async def delete_all(self) -> None:
        """Удалить все записи BattleRecord."""
        query = text("""
            DELETE FROM battle_record
        """)
        await self.session.execute(query)
        await self.session.commit()

    async def delete_by_id(self, battle_record_id: int) -> BattleRecord | None:
        """Удалить запись BattleRecord по ID."""
        query = text("""
            DELETE FROM battle_record
            WHERE id = :id
            RETURNING id, subscribe_id, user1_score, user2_score, 
                      user1_get_crowns, user2_get_crowns, 
                      user1_card_ids, user2_card_ids, replay
        """)
        result = await self.session.execute(query, {"id": battle_record_id})
        row = result.fetchone()
        await self.session.commit()
        if row:
            return BattleRecord(
                id=row.id,
                subscribe_id=row.subscribe_id,
                user1_score=row.user1_score,
                user2_score=row.user2_score,
                user1_get_crowns=row.user1_get_crowns,
                user2_get_crowns=row.user2_get_crowns,
                user1_card_ids=row.user1_card_ids,
                user2_card_ids=row.user2_card_ids,
                replay=row.replay
            )
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
            dao = BattleRecordDao(session)

            # Пример создания записи
            new_battle_record = await dao.create({
                "subscribe_id": 1,
                "user1_score": 10,
                "user2_score": 8,
                "user1_get_crowns": 3,
                "user2_get_crowns": 2,
                "user1_card_ids": [1, 2],
                "user2_card_ids": [3, 4],
                "replay": "replay_url",
            })
            print("Created:", new_battle_record)

            # Пример получения по ID
            battle_record = await dao.get_by_id(new_battle_record.id)
            print("Fetched by ID:", battle_record)

            # Пример получения всех записей
            all_battle_records = await dao.get_all()
            print("All battle records:", all_battle_records)

            # Пример обновления записи
            updated_battle_record = await dao.update_by_id(new_battle_record.id, {
                "user1_score": 12,
                "user2_score": 10,
            })
            print("Updated:", updated_battle_record)

            # Пример удаления по ID
            deleted_battle_record = await dao.delete_by_id(new_battle_record.id)
            print("Deleted:", deleted_battle_record)

            # Пример удаления всех записей
            await dao.delete_all()
            print("All battle records deleted.")

    asyncio.run(main())
