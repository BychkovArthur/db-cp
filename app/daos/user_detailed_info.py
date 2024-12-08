from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import UserDetailedInfo


class UserDetailedInfoDao:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, user_detailed_info: dict) -> UserDetailedInfo:
        """Создать запись UserDetailedInfo."""
        query = text("""
            INSERT INTO user_detailed_info (crowns, max_crowns, clan_id)
            VALUES (:crowns, :max_crowns, :clan_id)
            RETURNING id, crowns, max_crowns, clan_id
        """)
        result = await self.session.execute(query, user_detailed_info)
        row = result.fetchone()
        return UserDetailedInfo(
            id=row.id,
            crowns=row.crowns,
            max_crowns=row.max_crowns,
            clan_id=row.clan_id
        )

    async def get_by_id(self, user_detailed_info_id: int) -> UserDetailedInfo | None:
        """Получить запись UserDetailedInfo по ID."""
        query = text("""
            SELECT id, crowns, max_crowns, clan_id
            FROM user_detailed_info
            WHERE id = :id
        """)
        result = await self.session.execute(query, {"id": user_detailed_info_id})
        row = result.fetchone()
        if row:
            return UserDetailedInfo(
                id=row.id,
                crowns=row.crowns,
                max_crowns=row.max_crowns,
                clan_id=row.clan_id
            )
        return None
    

    async def get_by_ids(self, user_detailed_info_ids: list[int]) -> list[UserDetailedInfo] | None:
        """Получить записи UserDetailedInfo по списку ID."""
        if not user_detailed_info_ids:
            return None
        
        query = text("""
            SELECT id, crowns, max_crowns, clan_id
            FROM user_detailed_info
            WHERE id = ANY(:ids)
        """)
        result = await self.session.execute(query, {"ids": tuple(user_detailed_info_ids)})
        rows = result.fetchall()
        
        if rows:
            return [
                UserDetailedInfo(
                    id=row.id,
                    crowns=row.crowns,
                    max_crowns=row.max_crowns,
                    clan_id=row.clan_id
                )
                for row in rows
            ]
        return None

    async def get_all(self) -> list[UserDetailedInfo]:
        """Получить все записи UserDetailedInfo."""
        query = text("""
            SELECT id, crowns, max_crowns, clan_id
            FROM user_detailed_info
            ORDER BY id
        """)
        result = await self.session.execute(query)
        rows = result.fetchall()
        return [
            UserDetailedInfo(
                id=row.id,
                crowns=row.crowns,
                max_crowns=row.max_crowns,
                clan_id=row.clan_id
            ) for row in rows
        ]

    async def update_by_id(self, user_detailed_info_id: int, updated_data: dict) -> UserDetailedInfo | None:
        """Обновить запись UserDetailedInfo по ID."""
        query = text("""
            UPDATE user_detailed_info
            SET crowns = :crowns,
                max_crowns = :max_crowns,
                clan_id = :clan_id
            WHERE id = :id
            RETURNING id, crowns, max_crowns, clan_id
        """)
        result = await self.session.execute(query, {**updated_data, "id": user_detailed_info_id})
        row = result.fetchone()
        await self.session.commit()
        if row:
            return UserDetailedInfo(
                id=row.id,
                crowns=row.crowns,
                max_crowns=row.max_crowns,
                clan_id=row.clan_id
            )
        return None

    async def delete_all(self) -> None:
        """Удалить все записи UserDetailedInfo."""
        query = text("""
            DELETE FROM user_detailed_info
        """)
        await self.session.execute(query)
        await self.session.commit()

    async def delete_by_id(self, user_detailed_info_id: int) -> UserDetailedInfo | None:
        """Удалить запись UserDetailedInfo по ID."""
        query = text("""
            DELETE FROM user_detailed_info
            WHERE id = :id
            RETURNING id, crowns, max_crowns, clan_id
        """)
        result = await self.session.execute(query, {"id": user_detailed_info_id})
        row = result.fetchone()
        await self.session.commit()
        if row:
            return UserDetailedInfo(
                id=row.id,
                crowns=row.crowns,
                max_crowns=row.max_crowns,
                clan_id=row.clan_id
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
            dao = UserDetailedInfoDao(session)

            new_user_detailed_info = await dao.create({
                "crowns": 100,
                "max_crowns": 200,
                "clan_id": 1
            })
            print("Created:", new_user_detailed_info)

            user_detailed_info = await dao.get_by_id(new_user_detailed_info.id)
            print("Fetched by ID:", user_detailed_info)

            all_user_detailed_info = await dao.get_all()
            print("All user detailed info:", all_user_detailed_info)

            updated_user_detailed_info = await dao.update_by_id(new_user_detailed_info.id, {
                "crowns": 150,
                "max_crowns": 250,
            })
            print("Updated:", updated_user_detailed_info)

            deleted_user_detailed_info = await dao.delete_by_id(new_user_detailed_info.id)
            print("Deleted:", deleted_user_detailed_info)

            await dao.delete_all()
            print("All user detailed info deleted.")

    asyncio.run(main())
