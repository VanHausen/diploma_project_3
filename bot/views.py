from rest_framework import permissions, generics
from rest_framework.request import Request
from rest_framework.response import Response

from bot.models import TgUser
from bot.serializers import TgUserSerializer
from bot.tg.client import TgClient
from todolist import settings


class VerificationView(generics.UpdateAPIView):
#    model = TgUser
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TgUserSerializer

    def update(self, request, *args, **kwargs):
        serializer: TgUserSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        tg_user = serializer.save()
        TgClient(settings.BOT_TOKEN).send_message(
            chat_id=tg_user.chat_id,
            text='verification has been complete'
        )
