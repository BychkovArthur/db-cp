from clashroyale.official_api import Client
import os
from dotenv import load_dotenv
from app.daos.battle_record import BattleRecordDao
from app.daos.subscribe import SubscribeDao
from app.daos.user import UserDao
from app.daos.user_detailed_info import UserDetailedInfoDao
from datetime import datetime

from loguru import logger

import pytz

load_dotenv()

token = os.getenv("CLASH_ROYALE_API_TOKEN")
api_client = Client(token=token, is_async=True, url='https://proxy.royaleapi.dev/v1')

class ClashRoyaleApiService:

    @staticmethod
    async def fetch_battles(session):
        subscriptions = await SubscribeDao(session).get_all()

        for subscribe in subscriptions:
            user1_tag = (await UserDao(session).get_by_id(subscribe.user_id1)).tag.upper()
            user2_tag = (await UserDao(session).get_by_id(subscribe.user_id2)).tag.upper()
            battles = await api_client.get_player_battles(user1_tag, limit=3)
            print("Fetch ", len(battles))
            
            for battle in battles:
                battle_time = battle['battleTime']
                
                team = battle['team'][0]
                opponent = battle['opponent'][0]
                
                team_tag = team['tag'][1:].upper()
                opponent_tag = opponent['tag'][1:].upper()
                
                team_crowns = team['crowns']
                opponet_crowns = opponent['crowns']
                
                team_trophy_change = team.get('trophyChange', 0)
                opponent_trophy_change = opponent.get('trophyChange', 0)
                
                if (team_tag, opponent_tag)  == (user1_tag, user2_tag):
                    print(f"Match found: {user1_tag} vs {user2_tag}, time = {battle_time}")
                    battle_time = datetime.strptime(battle_time, '%Y%m%dT%H%M%S.%f%z')
                    battle_time = battle_time.replace(tzinfo=pytz.utc)
                    battle_time = battle_time.astimezone(pytz.utc).replace(tzinfo=None)
                                        
                    exists = await BattleRecordDao(session).exists_record(subscribe.id, battle_time)
                    if not exists:
                        record = {
                            'subscribe_id': subscribe.id,
                            'time': battle_time,
                            'user1_score': team_crowns,
                            'user2_score': opponet_crowns,
                            'user1_get_crowns': team_trophy_change,
                            'user2_get_crowns': opponent_trophy_change,
                            'user1_card_ids': [],
                            'user2_card_ids': [],
                            'replay': 'some-ref',
                            'winner_id': subscribe.user_id1 if team_crowns > opponet_crowns else subscribe.user_id2
                        }
                        record = await BattleRecordDao(session).create(record)
                        print(f'Record {record} created')
    
    
    @staticmethod
    async def fetch_user_detailed_info(session):
        users = await UserDao(session).get_all()
        users_detailed_info = await UserDetailedInfoDao(session).get_all()
        
        detailed_info_by_id = {
            info.id : info for info in users_detailed_info
        }
        
        for user in users:
            if user.user_detailed_info_id not in detailed_info_by_id:
                logger.error(f"User with id = {user.id} has no detailed info!!!")
                continue
            user_detailed_info = detailed_info_by_id[user.user_detailed_info_id]
            
            player = await api_client.get_player(user.tag)
            
            old_user_detailed_info = {
                "crowns": user_detailed_info.crowns,
                "max_crowns": user_detailed_info.max_crowns,
            }
            new_user_detailed_info = {
                "crowns" : player["trophies"],
                "max_crowns": player['bestTrophies'],
            }
            
            if old_user_detailed_info != new_user_detailed_info:
                updated_user_detailed_info = await UserDetailedInfoDao(session).update_by_id(
                        user_detailed_info_id=user_detailed_info.id,
                        updated_data={**new_user_detailed_info, "clan_id": user_detailed_info.clan_id}
                    )
                logger.info(f"User with id = {user.id} has been updated. His detailed info: {updated_user_detailed_info}!!!")
            
            
            
            
