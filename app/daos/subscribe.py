from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import Subscribe


class SubscribeDao:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, subscribe: dict) -> Subscribe:
        """Создать запись Subscribe."""
        query = text("""
            INSERT INTO subscribe (user_id1, user_id2, battle_type_id)
            VALUES (:user_id1, :user_id2, :battle_type_id)
            RETURNING id, user_id1, user_id2, battle_type_id
        """)
        result = await self.session.execute(query, {
            "user_id1": subscribe["user_id1"],
            "user_id2": subscribe["user_id2"],
            "battle_type_id": subscribe["battle_type_id"],
        })
        row = result.fetchone()
        await self.session.commit()
        return Subscribe(id=row.id, user_id1=row.user_id1, user_id2=row.user_id2, battle_type_id=row.battle_type_id)
    
    async def get_by_user_id1(self, user_id1: int) -> list[Subscribe] | None:
        """Получить записи по user_id1"""
        query = text("""
            SELECT id, user_id1, user_id2, battle_type_id
            FROM subscribe
            WHERE user_id1 = :user_id1
        """)
        result = await self.session.execute(query, {"user_id1": user_id1})
        rows = result.fetchall()
        subscriptions = []
        for row in rows:
            subscriptions.append(Subscribe(id=row.id, user_id1=row.user_id1, user_id2=row.user_id2, battle_type_id=row.battle_type_id))
        return subscriptions

    async def get_by_id(self, subscribe_id: int) -> Subscribe | None:
        """Получить запись Subscribe по ID."""
        query = text("""
            SELECT id, user_id1, user_id2, battle_type_id
            FROM subscribe
            WHERE id = :id
        """)
        result = await self.session.execute(query, {"id": subscribe_id})
        row = result.fetchone()
        if row:
            return Subscribe(id=row.id, user_id1=row.user_id1, user_id2=row.user_id2, battle_type_id=row.battle_type_id)
        return None
    
    async def get_by_triplet(self, user_id1: int, user_id2: int, battle_type_id: int) -> Subscribe | None:
        """Получить запись Subscribe по ID."""
        query = text("""
            SELECT id, user_id1, user_id2, battle_type_id
            FROM subscribe
            WHERE
                user_id1 = :user_id1 AND
                user_id2 = :user_id2 AND
                battle_type_id = :battle_type_id
        """)
        result = await self.session.execute(query, {"user_id1": user_id1, "user_id2": user_id2, "battle_type_id": battle_type_id})
        row = result.fetchone()
        if row:
            return Subscribe(id=row.id, user_id1=row.user_id1, user_id2=row.user_id2, battle_type_id=row.battle_type_id)
        return None

    async def get_all(self) -> list[Subscribe]:
        """Получить все записи Subscribe."""
        query = text("""
            SELECT id, user_id1, user_id2, battle_type_id
            FROM subscribe
            ORDER BY id
        """)
        result = await self.session.execute(query)
        rows = result.fetchall()
        return [Subscribe(id=row.id, user_id1=row.user_id1, user_id2=row.user_id2, battle_type_id=row.battle_type_id) for row in rows]

    async def update_by_id(self, subscribe_id: int, updated_data: dict) -> Subscribe | None:
        """Обновить запись Subscribe по ID."""
        query = text("""
            UPDATE subscribe
            SET user_id1 = :user_id1, user_id2 = :user_id2, battle_type_id = :battle_type_id
            WHERE id = :id
            RETURNING id, user_id1, user_id2, battle_type_id
        """)
        result = await self.session.execute(query, {
            "id": subscribe_id,
            "user_id1": updated_data["user_id1"],
            "user_id2": updated_data["user_id2"],
            "battle_type_id": updated_data["battle_type_id"],
        })
        row = result.fetchone()
        await self.session.commit()
        if row:
            return Subscribe(id=row.id, user_id1=row.user_id1, user_id2=row.user_id2, battle_type_id=row.battle_type_id)
        return None

    async def delete_all(self) -> None:
        """Удалить все записи Subscribe."""
        query = text("""
            DELETE FROM subscribe
        """)
        await self.session.execute(query)
        await self.session.commit()

    async def delete_by_id(self, subscribe_id: int) -> Subscribe | None:
        """Удалить запись Subscribe по ID."""
        query = text("""
            DELETE FROM subscribe
            WHERE id = :id
            RETURNING id, user_id1, user_id2, battle_type_id
        """)
        result = await self.session.execute(query, {"id": subscribe_id})
        row = result.fetchone()
        await self.session.commit()
        if row:
            return Subscribe(id=row.id, user_id1=row.user_id1, user_id2=row.user_id2, battle_type_id=row.battle_type_id)
        return None
    
    async def subscribe_user(self, user_id1: int, user_id2: int, battle_type_id: int) -> Subscribe | None:
        """Подписаться на другого пользователя."""
        
        query = text("""
            SELECT id FROM subscribe
            WHERE user_id1 = :user_id1 AND user_id2 = :user_id2 AND battle_type_id = :battle_type_id
        """)
        result = await self.session.execute(query, {
            "user_id1": user_id1,
            "user_id2": user_id2,
            "battle_type_id": battle_type_id,
        })
        if result.fetchone():
            return None

        subscribe = Subscribe(user_id1=user_id1, user_id2=user_id2, battle_type_id=battle_type_id)
        self.session.add(subscribe)
        await self.session.commit()
        await self.session.refresh(subscribe)
        return subscribe

    async def unsubscribe_user(self, user_id1: int, user_id2: int, battle_type_id: int) -> bool:
        """Отписаться от другого пользователя."""

        query = text("""
            DELETE FROM subscribe
            WHERE user_id1 = :user_id1 AND user_id2 = :user_id2 AND battle_type_id = :battle_type_id
        """)
        result = await self.session.execute(query, {
            "user_id1": user_id1,
            "user_id2": user_id2,
            "battle_type_id": battle_type_id,
        })
        await self.session.commit()
        if result.rowcount > 0:
            return True
        return False

    async def get_subscriptions_by_user(self, user_id1: int) -> list[Subscribe]:
        """Получить все подписки пользователя."""
        query = text("""
            SELECT id, user_id1, user_id2, battle_type_id
            FROM subscribe
            WHERE user_id1 = :user_id1
            ORDER BY id
        """)
        result = await self.session.execute(query, {"user_id1": user_id1})
        rows = result.fetchall()
        return [Subscribe(id=row.id, user_id1=row.user_id1, user_id2=row.user_id2, battle_type_id=row.battle_type_id) for row in rows]


if __name__ == "__main__":
    import asyncio
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker

    async def main():
        DATABASE_URL = "postgresql+asyncpg://user:password@localhost/testdb"
        engine = create_async_engine(DATABASE_URL, echo=True)
        async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

        async with async_session() as session:
            dao = SubscribeDao(session)

            # Пример создания записи
            new_subscribe = await dao.create({"user_id1": 1, "user_id2": 2, "battle_type_id": 1})
            print("Created:", new_subscribe)

            # Пример получения по ID
            subscribe = await dao.get_by_id(new_subscribe.id)
            print("Fetched by ID:", subscribe)

            # Пример получения всех записей
            all_subscriptions = await dao.get_all()
            print("All subscriptions:", all_subscriptions)

            # Пример обновления записи
            updated_subscribe = await dao.update_by_id(new_subscribe.id, {
                "user_id1": 1,
                "user_id2": 3,
                "battle_type_id": 2,
            })
            print("Updated:", updated_subscribe)

            # Пример удаления по ID
            deleted_subscribe = await dao.delete_by_id(new_subscribe.id)
            print("Deleted:", deleted_subscribe)

            # Пример удаления всех записей
            await dao.delete_all()
            print("All records deleted.")

    asyncio.run(main())
