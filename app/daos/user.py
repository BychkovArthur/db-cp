from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User


class UserDao:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, user: dict) -> User:
        """Создать запись User."""
        query = text("""
            INSERT INTO public.user (email, password, name, tag, user_detailed_info_id,is_super_user)
            VALUES (:email, :password, :name, :tag, :user_detailed_info_id, FALSE)
            RETURNING id, email, password, name, tag, user_detailed_info_id, is_super_user
        """)
        result = await self.session.execute(query, user)
        row = result.fetchone()
        return User(
            id=row.id,
            email=row.email,
            password=row.password,
            name=row.name,
            tag=row.tag,
            user_detailed_info_id=row.user_detailed_info_id,
            is_super_user=False
        )
    
    async def get_by_email(self, email: str) -> User | None:
        """Получить запись User по email."""
        query = text("""
            SELECT id, email, password, name, tag, user_detailed_info_id, is_super_user
            FROM public.user
            WHERE email = :email
        """)
        result = await self.session.execute(query, {"email": email})
        row = result.fetchone()
        if row:
            return User(
                id=row.id,
                email=row.email,
                password=row.password,
                name=row.name,
                tag=row.tag,
                user_detailed_info_id=row.user_detailed_info_id,
                is_super_user=row.is_super_user
            )
        return None

    async def get_by_id(self, user_id: int) -> User | None:
        """Получить запись User по ID."""
        query = text("""
            SELECT id, email, password, name, tag, user_detailed_info_id, is_super_user
            FROM public.user
            WHERE id = :id
        """)
        result = await self.session.execute(query, {"id": user_id})
        row = result.fetchone()
        if row:
            return User(
                id=row.id,
                email=row.email,
                password=row.password,
                name=row.name,
                tag=row.tag,
                user_detailed_info_id=row.user_detailed_info_id,
                is_super_user=row.is_super_user
            )
        return None

    async def get_all(self) -> list[User]:
        """Получить все записи User."""
        query = text("""
            SELECT id, email, password, name, tag, user_detailed_info_id, is_super_user
            FROM public.user
            ORDER BY id
        """)
        result = await self.session.execute(query)
        rows = result.fetchall()
        return [
            User(
                id=row.id,
                email=row.email,
                password=row.password,
                name=row.name,
                tag=row.tag,
                user_detailed_info_id=row.user_detailed_info_id,
                is_super_user=row.is_super_user
            ) for row in rows
        ]
        
    async def get_all_except_self(self, user_id: int) -> list[User]:
        """Получить все записи User."""
        query = text("""
            SELECT id, email, password, name, tag, user_detailed_info_id, is_super_user
            FROM public.user
            WHERE id <> :id
            ORDER BY id
        """)
        result = await self.session.execute(query, {"id" : user_id})
        rows = result.fetchall()
        return [
            User(
                id=row.id,
                email=row.email,
                password=row.password,
                name=row.name,
                tag=row.tag,
                user_detailed_info_id=row.user_detailed_info_id,
                is_super_user=row.is_super_user
            ) for row in rows
        ]

    async def update_by_id(self, user_id: int, updated_data: dict) -> User | None:
        """Обновить запись User по ID."""
        query = text("""
            UPDATE public.user
            SET email = :email,
                password = :password,
                name = :name,
                tag = :tag,
                user_detailed_info_id = :user_detailed_info_id
            WHERE id = :id
            RETURNING id, email, password, name, tag, user_detailed_info_id
        """)
        result = await self.session.execute(query, {**updated_data, "id": user_id})
        row = result.fetchone()
        await self.session.commit()
        if row:
            return User(
                id=row.id,
                email=row.email,
                password=row.password,
                name=row.name,
                tag=row.tag,
                user_detailed_info_id=row.user_detailed_info_id
            )
        return None

    async def delete_all(self) -> None:
        """Удалить все записи User."""
        query = text("""
            DELETE FROM user
        """)
        await self.session.execute(query)
        await self.session.commit()

    async def delete_by_id(self, user_id: int) -> User | None:
        """Удалить запись User по ID."""
        query = text("""
            DELETE FROM public.user
            WHERE id = :id
            RETURNING id, email, password, name, tag, user_detailed_info_id
        """)
        result = await self.session.execute(query, {"id": user_id})
        row = result.fetchone()
        await self.session.commit()
        if row:
            return User(
                id=row.id,
                email=row.email,
                password=row.password,
                name=row.name,
                tag=row.tag,
                user_detailed_info_id=row.user_detailed_info_id
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
            dao = UserDao(session)

            # Пример создания записи
            new_user = await dao.create({
                "email": "user@example.com",
                "password": "password123",
                "name": "John Doe",
                "tag": "JDoe",
                "user_detailed_info_id": 1
            })
            print("Created:", new_user)

            # Пример получения по ID
            user = await dao.get_by_id(new_user.id)
            print("Fetched by ID:", user)

            # Пример получения всех записей
            all_users = await dao.get_all()
            print("All users:", all_users)

            # Пример обновления записи
            updated_user = await dao.update_by_id(new_user.id, {
                "email": "new_email@example.com",
                "password": "newpassword123",
                "name": "Johnathan Doe",
                "tag": "JDoeUpdated",
                "user_detailed_info_id": 2
            })
            print("Updated:", updated_user)

            # Пример удаления по ID
            deleted_user = await dao.delete_by_id(new_user.id)
            print("Deleted:", deleted_user)

            # Пример удаления всех записей
            await dao.delete_all()
            print("All users deleted.")

    asyncio.run(main())
