import logging
from enum import Enum

import requests
from django.conf import settings

from bot.tg.dc import GetUpdatesResponse, SendMessageResponse


class Command(str, Enum):
    GET_UPDATES = "GetUpdates"
    GET_MESSAGE = "SendMessage"

class TgClient:
    def __init__(self, token: str | None = None):
        self.token = token if token else settings.BOT_TOKEN
        self.logger = logging.getLogger(__name__)

    def get_url(self, method: str) -> str:
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        data = self._get(Command.GET_UPDATES, offset=offset, timeout=timeout)
        return GetUpdatesResponse(**data)

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        data = self._get(Command.SET_MESSAGE, chat_id=chat_id, text=text)
        return SendMessageResponse(**data)

    def _get(self, command: Command, **params) -> dict:
        url = self.get_url(command)
        resp = requests.get(url, params=params)
        if not resp.ok:
            print(resp.json())
            raise ValueError
        return resp.json()