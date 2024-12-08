from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import BattleRecord


class BattleRecordDao:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, battle_record: dict) -> BattleRecord:
        query = text("""
            INSERT INTO battle_record (subscribe_id, user1_score, user2_score, 
                                      user1_get_crowns, user2_get_crowns, 
                                      user1_card_ids, user2_card_ids, replay, 
                                      time, winner_id)
            VALUES (:subscribe_id, :user1_score, :user2_score, 
                    :user1_get_crowns, :user2_get_crowns, 
                    :user1_card_ids, :user2_card_ids, :replay, 
                    :time, :winner_id)
            RETURNING id, subscribe_id, user1_score, user2_score, 
                      user1_get_crowns, user2_get_crowns, 
                      user1_card_ids, user2_card_ids, replay, 
                      time, winner_id
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
            replay=row.replay,
            time=row.time,
            winner_id=row.winner_id
        )

    async def get_by_id(self, battle_record_id: int) -> BattleRecord | None:
        query = text("""
            SELECT id, subscribe_id, user1_score, user2_score, 
                   user1_get_crowns, user2_get_crowns, 
                   user1_card_ids, user2_card_ids, replay, 
                   time, winner_id
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
                replay=row.replay,
                time=row.time,
                winner_id=row.winner_id
            )
        return None
    
    async def get_by_subscribe_ids(self, subscribe_ids: list[int]) -> list[BattleRecord] | None:
        query = text("""
            SELECT id, subscribe_id, user1_score, user2_score, 
                   user1_get_crowns, user2_get_crowns, 
                   user1_card_ids, user2_card_ids, replay, 
                   time, winner_id
            FROM battle_record
            WHERE subscribe_id = ANY(:subscribe_ids)
        """)
        result = await self.session.execute(query, {"subscribe_ids": subscribe_ids})
        rows = result.fetchall()
        records = []
        for row in  rows:
            records.append(BattleRecord(
                id=row.id,
                subscribe_id=row.subscribe_id,
                user1_score=row.user1_score,
                user2_score=row.user2_score,
                user1_get_crowns=row.user1_get_crowns,
                user2_get_crowns=row.user2_get_crowns,
                user1_card_ids=row.user1_card_ids,
                user2_card_ids=row.user2_card_ids,
                replay=row.replay,
                time=row.time,
                winner_id=row.winner_id
            ))
        return records

    async def get_all(self) -> list[BattleRecord]:
        query = text("""
            SELECT id, subscribe_id, user1_score, user2_score, 
                   user1_get_crowns, user2_get_crowns, 
                   user1_card_ids, user2_card_ids, replay, 
                   time, winner_id
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
                replay=row.replay,
                time=row.time,
                winner_id=row.winner_id
            ) for row in rows
        ]

    async def update_by_id(self, battle_record_id: int, updated_data: dict) -> BattleRecord | None:
        query = text("""
            UPDATE battle_record
            SET subscribe_id = :subscribe_id,
                user1_score = :user1_score,
                user2_score = :user2_score,
                user1_get_crowns = :user1_get_crowns,
                user2_get_crowns = :user2_get_crowns,
                user1_card_ids = :user1_card_ids,
                user2_card_ids = :user2_card_ids,
                replay = :replay,
                time = :time,
                winner_id = :winner_id
            WHERE id = :id
            RETURNING id, subscribe_id, user1_score, user2_score, 
                      user1_get_crowns, user2_get_crowns, 
                      user1_card_ids, user2_card_ids, replay, 
                      time, winner_id
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
                replay=row.replay,
                time=row.time,
                winner_id=row.winner_id
            )
        return None

    async def delete_by_id(self, battle_record_id: int) -> BattleRecord | None:
        query = text("""
            DELETE FROM battle_record
            WHERE id = :id
            RETURNING id, subscribe_id, user1_score, user2_score, 
                      user1_get_crowns, user2_get_crowns, 
                      user1_card_ids, user2_card_ids, replay, 
                      time, winner_id
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
                replay=row.replay,
                time=row.time,
                winner_id=row.winner_id
            )
        return None
    

    async def exists_record(self, subscribe_id: int, time):
        query = text("""
            SELECT 1
            FROM battle_record
            WHERE
                subscribe_id = :subscribe_id 
                AND time = :time
        """)
        result = await self.session.execute(query, {
            'subscribe_id': subscribe_id,
            'time': time,
        })
        return True if result.scalar() else False