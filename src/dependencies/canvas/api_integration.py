import os
import requests
from dotenv import load_dotenv

from src.settings.settings import BASE_DIR

load_dotenv(os.path.join(BASE_DIR, '../.env'))


class CanvasApiIntegration:
    __HEADERS = {'Authorization': os.getenv('CANVAS_ACCESS_TOKEN')}

    __BASE_API_URL = os.getenv('CANVAS_BASE_API_URL')

    def __request_login_id(self, user_id: int):
        response = requests.get(
            url=f'{self.__BASE_API_URL}/users/{user_id}/logins',
            headers=self.__HEADERS
        )

        if response.ok:
            return response.json()[0]['id']

    def __update_login_data(self, login_id: int, login_data: dict):
        response = requests.put(
            url=f'{self.__BASE_API_URL}/accounts/self/logins/{login_id}',
            headers=self.__HEADERS,
            params=login_data
        )

        return response.ok

    def sync_password(self, user_id: int | None, password: str) -> bool:
        login_id = self.__request_login_id(user_id) if user_id else None
        login_data = {'login[password]': password}

        return self.__update_login_data(login_id, login_data) if login_id else False
