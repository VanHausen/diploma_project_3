from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from bot.models import TgUser


class TgUserSerializer(serializers.ModelSerializer):
    tg_id = serializers.SlugField(source='chat_id', read_only=True)
#    username = serializers.PrimaryKeyRelatedField(source='username', read_only=True)
#    verification_code = serializers.CharField(write_only=True)

    class Meta:
        model = TgUser
        fields = ("tg_id", "username", "verification_code", "user_id")
        read_only_fields = ("tg_id", "username", "user_id")


    def validate_verification_code(self, value: str):
        try:
          self.instance = TgUser.objects.get(verification_code=value)
        except TgUser.DoesNotExist:
            raise ValidationError("Field code is incorrect")
        return value

    def update(self, instance, validated_data):
        self.instance.user = self.context['request'].user
        return super().update(instance, validated_data)
