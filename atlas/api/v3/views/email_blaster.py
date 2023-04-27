from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from atlas.apps.email_blaster.serializers import EmailSendRequestSerializer
from atlas.apps.email_blaster.services import EmailSendService, EmailTemplateService
from django.conf import settings


@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def send_email(request):
    serializer = EmailSendRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(data={'messages': serializer._errors},
                        status=status.HTTP_400_BAD_REQUEST)

    validated_request = serializer.validated_data
    email_template_service = EmailTemplateService()
    template = email_template_service.get_email_template(
        validated_request["email_template_id"])
    survei_url = f"{settings.FRONTEND_URL}/survei/{validated_request['survei_id']}"
    email_send_service = EmailSendService(
        email_body_with_placeholder=template.email_body,
        email_subject=template.email_subject,
        survei_url=survei_url,
        recipients=validated_request["recipients"]
    )

    email_send_service.send_email_batch(
        validated_request["wait_delay"], validated_request["batch_size"])
    return Response(status=status.HTTP_200_OK)


@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def preview_email(request):
    serializer = EmailSendRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(data={'messages': serializer._errors},
                        status=status.HTTP_400_BAD_REQUEST)

    validated_request = serializer.validated_data
    email_template_service = EmailTemplateService()
    template = email_template_service.get_email_template(
        validated_request["email_template_id"])
    survei_url = f"{settings.FRONTEND_URL}/survei/{validated_request['survei_id']}"
    email_send_service = EmailSendService(
        email_body_with_placeholder=template.email_body,
        email_subject=template.email_subject,
        survei_url=survei_url,
        recipients=validated_request["recipients"]
    )

    return Response(data={
        "email_body": email_send_service.email_body,
        "email_subject": email_send_service.email_subject,
        "recipients": email_send_service.recipients,
    }, status=status.HTTP_200_OK)
