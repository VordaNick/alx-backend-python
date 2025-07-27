from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsParticipantOfConversation(BasePermission):
    """
    Allows access only to authenticated users who are participants in the conversation.
    """

    def has_permission(self, request, view):
        # General check for all methods: user must be authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level permissions:
        Only participants can view, update, or delete messages/conversations.
        Assumes `obj` has `conversation.participants` relationship.
        """
        user = request.user

        # Ensure that the object has access to its conversation and participants
        try:
            participants = obj.conversation.participants.all()
        except AttributeError:
            # If the object *is* a conversation
            participants = obj.participants.all()

        # Only allow access if the user is a participant
        if user not in participants:
            return False

        # Explicitly allow specific methods
        if request.method in SAFE_METHODS:
            return True  # GET, HEAD, OPTIONS

        elif request.method in ['PUT', 'PATCH', 'DELETE']:
            return True  # Only participants can modify/delete

        elif request.method == 'POST':
            # Creation is allowed globally via has_permission, or override in the view if needed
            return True

        return False
