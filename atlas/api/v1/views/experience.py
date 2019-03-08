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


class AbstractExperienceListCreateView(ListCreateAPIView):
    """
    Abstract class for get list or create api view for experience.
    For now we set the permission to only the owner that can use.
    """
    permission_classes = (IsOwnerOfExperience,)
    model_class = None
    lookup_field = 'username'

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
            User, **{self.lookup_field: self.kwargs[self.lookup_field]})
        Klass = self.get_model_class()
        return Klass.objects.filter(owner=user)

    def perform_create(self, serializer):
        """
        perform save instance, inject owner because in serializer,
        the owner field is read only
        """
        serializer.save(owner=self.request.user)


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
        return Klass.objects.filter(owner=user)


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

    get:
    Return list of education owned by user
    """
    model_class = Education
    serializer_class = EducationSerializer


class EducationDetailView(AbstractExperienceDetailView):
    """
    get:
    put:
    patch:
    delete:
    """
    model_class = Education
    serializer_class = EducationSerializer