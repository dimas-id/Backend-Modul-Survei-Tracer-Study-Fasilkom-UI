from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from atlas.apps.email_blaster.models import EmailTemplate
from atlas.apps.email_blaster.serializers import EmailTemplateSerializer


@permission_classes([IsAuthenticated, IsAdminUser])
class EmailTemplateListView(generics.ListAPIView):
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer


@permission_classes([IsAuthenticated, IsAdminUser])
class EmailTemplateCreateView(generics.CreateAPIView):
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer


@permission_classes([IsAuthenticated, IsAdminUser])
class EmailTemplateUpdateView(generics.RetrieveUpdateAPIView):
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer


@permission_classes([IsAuthenticated, IsAdminUser])
class EmailTemplateDeleteView(generics.DestroyAPIView):
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer
