from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from atlas.apps.experience.permissions import IsOwnerOfExperience
from atlas.apps.experience.serializers import EducationSerializer, PositionSerializer
from atlas.apps.experience.models import Position, Education
from atlas.apps.experience.services import ExperienceService
from atlas.libs import redis

User = get_user_model()
experience_service = ExperienceService()


class AbstractExperienceListCreateView(ListCreateAPIView):
    """
    Abstract class for get list or create api view for experience.
    For now we set the permission to only the owner that can use.
    """
    permission_classes = (IsOwnerOfExperience,)
    model_class = None
    lookup_field = 'user_id'

    def get_model_class(self):
        """
        Return model class defined
        """
        assert self.model_class is not None, 'Attribute model_class is not implemented'
        return self.model_class

    def get_queryset(self):
        """
        We can get the user from request.user, but we want to ensure that it is flexible
        when we change it to public user. Therefore, we query the user.
        Return a queryset based on user
        """
        user = get_object_or_404(
            User, id=self.kwargs[self.lookup_field])
        Klass = self.get_model_class()
        return Klass.objects.filter(user=user)

    def perform_create(self, serializer):
        """
        perform save instance, inject owner because in serializer,
        the owner field is read only
        """
        serializer.save(user=self.request.user)


class AbstractExperienceDetailView(RetrieveUpdateDestroyAPIView):
    """
    Abstract class for retrieve, update, delete api view for experience.
    For now we set the permission to only the owner that can use.
    """
    permission_classes = (IsOwnerOfExperience,)
    model_class = None

    def get_model_class(self):
        """
        Return model class defined
        """
        assert self.model_class is not None, 'Attribute model_class is not implemented'
        return self.model_class

    def get_queryset(self):
        user = self.request.user
        Klass = self.get_model_class()
        return Klass.objects.filter(user=user)


class PositionListCreateView(AbstractExperienceListCreateView):
    """
    post:
    Create position

    get:
    Return list of position owned by user
    """
    model_class = Position
    serializer_class = PositionSerializer


class PositionDetailView(AbstractExperienceDetailView):
    """
    get:
    put:
    patch:
    delete:
    """
    model_class = Position
    serializer_class = PositionSerializer


class EducationListCreateView(AbstractExperienceListCreateView):
    """
    post:
    Create education
    overriding post method to verify user
    """

    def perform_create(self, serializer):
        """
        perform save instance, inject owner because in serializer,
        the owner field is read only
        """
        obj = serializer.save(user=self.request.user)
        for education in obj:
            redis.enqueue(experience_service.verify_user_registration, education=education)


    """

    get:
    Return list of education owned by user
    """
    model_class = Education
    serializer_class = EducationSerializer

    """
    Override serializer to force many=True on create
    """
    def get_serializer(self, data=None, instance=None, many=False, partial=False):
        serializer = super(EducationListCreateView, self)\
            .get_serializer(instance=instance,data=data, many=True, partial=partial)
        serializer.is_valid()
        return serializer


class EducationDetailView(AbstractExperienceDetailView):
    """
    get:
    put:
    patch:
    delete:
    """
    model_class = Education
    serializer_class = EducationSerializer


