from clashroyale.official_api import Client
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("CLASH_ROYALE_API_TOKEN")

api_client = Client(token=token, is_async=True, url='https://proxy.royaleapi.dev/v1')