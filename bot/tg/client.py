import logging
from enum import Enum

import requests
import resp as resp
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

#    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
#        data = self._get(Command.GET_UPDATES, offset=offset, timeout=timeout)
#        return GetUpdatesResponse.Schema().load(data.json())
#
#    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
#        data = self._get(Command.SEND_MESSAGE, chat_id=chat_id, text=text)
#        return SendMessageResponse.Schema().load(data.json())

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        url = self.get_url("getUpdates")
        resp = requests.get(url, params={"offset": offset, "timeout": timeout})
        return GetUpdatesResponse.Schema().load(resp.json())

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        url = self.get_url("sendMessage")
        resp = requests.post(url, json={"chat_id": chat_id, "text": text})
        return SendMessageResponse.Schema().load(resp.json())

    def _get(self, command: Command, **params) -> dict:
        url = self.get_url(command)
        resp = requests.get(url, params=params)
        if not resp.ok:
            print(resp.json())
            raise ValueError
        return resp.json()