from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse

from datetime import timedelta
from typing import Annotated

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.daos import battle_record, subscribe, user

from app.models.user import User as UserModel
from app.schemas.battle_record import BattleRecordOut, AggregatedBattleRecord



class BattleRecordService:
    @staticmethod
    async def get_battle_records(current_user: UserModel, session: AsyncSession) -> list[BattleRecordOut]:
        user_subscriptions = await subscribe.SubscribeDao(session).get_by_user_id1(current_user.id)
        subscribe_ids = [subscription.id for subscription in user_subscriptions]
        battle_records = await battle_record.BattleRecordDao(session).get_by_subscribe_ids(subscribe_ids)
        
        subscribe_by_id = {subscribe.id : subscribe for subscribe in user_subscriptions}
        
        result = []
        for _battle_record in battle_records:
            opponent = await user.UserDao(session).get_by_id(subscribe_by_id[_battle_record.subscribe_id].user_id2)
            
            result.append(BattleRecordOut(
                name1=current_user.name,
                name2=opponent.name,
                user1_score=_battle_record.user1_score,
                user2_score=_battle_record.user2_score,
                user1_get_crowns=_battle_record.user1_get_crowns,
                user2_get_crowns=_battle_record.user2_get_crowns,
                is_user1_win=(_battle_record.winner_id == current_user.id)
            ))
        
        return result
    

    @staticmethod
    async def get_aggregated_battle_records(current_user: UserModel, session: AsyncSession) -> list[AggregatedBattleRecord]:
        records = await BattleRecordService.get_battle_records(current_user, session)
        
        from collections import defaultdict
        record_groups = defaultdict(lambda: {'score1': 0, 'score2': 0})
        
        for record in records:
            pair = (record.name1, record.name2)
            if record.is_user1_win:
                record_groups[pair]['score1'] += 1
            else:
                record_groups[pair]['score2'] += 1
        
        aggregated_records = []
        for (name1, name2), scores in record_groups.items():
            aggregated_records.append(
                AggregatedBattleRecord(
                    name1=name1,
                    name2=name2,
                    score1=scores['score1'],
                    score2=scores['score2']
                )
            )
        
        return aggregated_records