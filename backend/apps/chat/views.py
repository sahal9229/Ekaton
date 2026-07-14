from core.responses import success_response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .matchmaking import start_chat
from .serializers import EndChatSerializer
from .services import end_private_chat_room, get_private_chat_room


class StartChatAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        result = start_chat(request.user)

        return success_response(message=result["message"], data=result)


class EndChatAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = EndChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        room = get_private_chat_room(serializer.validated_data["room_id"])

        end_private_chat_room(room)

        return success_response(message="Chat ended successfully")
