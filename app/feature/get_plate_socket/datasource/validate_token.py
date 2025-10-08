import requests
from dotenv import load_dotenv
import os

load_dotenv()

class ValidateToken:
    def token(self, token: str) -> int:
        try:
            url = os.getenv("API_URL")

            headers = {
                "Authorization": f"Bearer {token}",
                "accept": "application/json"
            }

            response = requests.head(f'{url}me', headers=headers)
            return response.status_code
        except Exception as e:
            print(f"❌ Erro: {e}")
            return 400