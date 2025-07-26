from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Message, Conversation
from .serializers import MessageSerializer
from .permissions import IsParticipantOfConversation
from rest_framework.exceptions import PermissionDenied

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        """
        Return messages in a conversation if the user is a participant.
        URL must include ?conversation_id=<id>
        """
        conversation_id = self.request.query_params.get("conversation_id")
        user = self.request.user

        if not conversation_id:
            return Message.objects.none()

        conversation = get_object_or_404(Conversation, id=conversation_id)

        if user not in conversation.participants.all():
            raise PermissionDenied("You are not a participant in this conversation.")

        return Message.objects.filter(conversation=conversation)

    def perform_create(self, serializer):
        """
        Only allow message creation if user is a participant of the conversation.
        """
        conversation_id = self.request.data.get("conversation_id")
        conversation = get_object_or_404(Conversation, id=conversation_id)

        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not allowed to send messages in this conversation.")

        serializer.save(sender=self.request.user, conversation=conversation)

