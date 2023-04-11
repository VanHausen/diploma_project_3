from django.conf import settings
from django.core.management import BaseCommand
from logger import logger

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from goals.models import Goal


class Command(BaseCommand):
    help = "run bot"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(settings.BOT_TOKEN)

    def handle(self, *args, **kwargs):
        offset = 0

        logger.info('Bot start handling')
        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(item.message)


    def handle_user_without_verification(self, msg: Message, tg_user: TgUser):
        self.tg_client.send_message(tg_user.tg_id, 'Heloo!')

        code = tg_user.set_verification_code()
        self.tg_client.send_message(tg_user.tg_id, f'verification code: {code}')


    def fetch_tasks(self, msg: Message, tg_user: TgUser):
        gls = Goal.objects.filter(user=tg_user.user)
        if gls.count() > 0:
            resp_msg = [f"#{item.id} {item.title}" for item in gls]
            self.tg_client.send_message(msg.chat.id, "\n".join(resp_msg))
        else:
            self.tg_client.send_message(msg.chat.id, "[goals list is empty]")

    def handle_verified_user(self, msg: Message, tg_user: TgUser):
        if not msg.text:
            return
        if "/goals" in msg.text:
            self.fetch_tasks(msg, tg_user)
        else:
            self.tg_client.send_message(msg.chat.id, "[unknown command]")

    def handle_message(self, msg: Message):
        tg_user, created = TgUser.objects.get_or_create(
            tg_id=msg.from_.id,
            defaults={
                "tg_chat_id": msg.chat.id,
                #"username": msg.from_.username,
            },
        )
        if tg_user.user:
            logger.info("Authorized")
        else:
            logger.info("Unauthorized")