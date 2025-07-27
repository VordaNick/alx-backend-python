from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Message, Conversation
from .serializers import MessageSerializer
from .filters import MessageFilter
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import CustomPagination

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter
    pagination_class = CustomPagination

    def get_queryset(self):
        conversation_id = self.request.query_params.get("conversation_id")
        user = self.request.user

        if not conversation_id:
            return Message.objects.none()

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            self.permission_denied(self.request, message="Conversation not found.")

        if user not in conversation.participants.all():
            self.permission_denied(self.request, message="You are not a participant.")

        return Message.objects.filter(conversation=conversation)

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get("conversation_id")
        user = request.user

        if not conversation_id:
            return Response({"detail": "conversation_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"detail": "Conversation not found."}, status=status.HTTP_404_NOT_FOUND)

        if user not in conversation.participants.all():
            return Response({"detail": "You are not allowed to send messages in this conversation."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=user, conversation=conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
