from rest_framework import serializers

from .models import PrivateChatRoom, PrivateMessage, Report


class PrivateChatRoomSerializer(serializers.ModelSerializer):
    user_one_email = serializers.EmailField(source="user_one.email", read_only=True)
    user_two_email = serializers.EmailField(source="user_two.email", read_only=True)

    class Meta:
        model = PrivateChatRoom
        fields = [
            "id",
            "status",
            "user_one_email",
            "user_two_email",
            "reveal_completed",
            "created_at",
        ]


class PrivateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateMessage
        model = PrivateMessage
        fields = [
            "id",
            "room",
            "sender",
            "message",
            "message_type",
            "is_read",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = [
            "id",
            "room",
            "reporter",
            "reported_user",
            "reason",
            "description",
            "evidence_url",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class StartChatSerializer(serializers.Serializer):
    pass


class EndChatSerializer(serializers.Serializer):
    room_id = serializers.CharField()


class RevealRequestSerializer(serializers.Serializer):
    room_id = serializers.CharField()


class RevealResponseSerializer(serializers.Serializer):
    reveal_request_id = serializers.UUIDField()
    status = serializers.ChoiceField(
        choices=(
            ("accepted", "accepted"),
            ("rejected", "rejected"),
        )
    )
