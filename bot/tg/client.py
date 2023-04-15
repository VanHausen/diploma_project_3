import logging

import requests

from bot.tg.dc import GetUpdatesResponse, SendMessageResponse


class TgClient:
    def __init__(self, token: str):
        self.token = token

    def get_url(self, method: str) -> str:
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
      url = self.get_url('getUpdates')
      response = requests.get(url, params={'offset': offset, 'timeout': timeout})
      return GetUpdatesResponse(**response.json())

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
       url = self._get('sendMessage')
       try:
           response = requests.post(url, json={
               'chat_id': chat_id,
               'text': text,
           })
       except:
           logging.error('Failed to get updates')
           raise
       else:
        return SendMessageResponse(**response.json())