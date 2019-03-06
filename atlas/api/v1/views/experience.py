from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from atlas.apps.experience.permissions import IsOwnerOfExperience
from atlas.apps.experience.serializers import EducationSerializer, PositionSerializer
from atlas.apps.experience.models import Position, Education

User = get_user_model()


class PositionListCreateView(ListCreateAPIView):
    """
    post:
    Create position

    get:
    Return list of position owned by user
    """
    permission_classes = (IsOwnerOfExperience,)
    serializer_class = PositionSerializer
    lookup_field = 'username'

    def get_queryset(self):
        """
        Return a queryset based on user
        """
        user = get_object_or_404(
            User, **{self.lookup_field: self.kwargs[self.lookup_field]})
        return Position.objects.filter(owner=user)


class EducationListCreateView(ListCreateAPIView):
    """
    post:
    Create education

    get:
    Return list of education owned by user
    """
    permissions_classes = (IsOwnerOfExperience,)
    serializer_class = EducationSerializer
    lookup_field = 'username'

    def get_queryset(self):
        """
        Return a queryset based on user
        """
        # we can user request.user, but we want to ensure that username is valid.
        # therefore, we query the user.
        user = get_object_or_404(
            User, **{self.lookup_field: self.kwargs[self.lookup_field]})
        return Position.objects.filter(owner=user)
