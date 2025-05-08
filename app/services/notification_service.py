from loguru import logger
from app.services.redis_service import redis_service

class BattleNotificationService:
    async def handle_new_battle(self, data: dict) -> None:
        """Handle new battle event"""
        try:
            user_id = data['user_id']
            user_name = data['user_name']
            opponent_name = data['opponent_name']
            user_score = data['user_score']
            opponent_score = data['opponent_score']
            is_win = data['is_win']
            
            result = "won" if is_win else "lost"
            message = f"New battle for {user_name}: {user_name} {result} against {opponent_name} ({user_score}-{opponent_score})"
            logger.info(message)
        except Exception as e:
            logger.error(f"Error handling battle notification: {e}")

battle_notification_service = BattleNotificationService()

# Подписываемся на события
async def setup_battle_notifications():
    await redis_service.subscribe('new_battle', battle_notification_service.handle_new_battle) 