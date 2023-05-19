from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from atlas.apps.email_blaster.serializers import CSVFilesSerializer
from atlas.apps.email_blaster.services import CSVEmailParser


@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def upload_email_csv(request):
    serializer = CSVFilesSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(data={'messages': serializer._errors},
                        status=status.HTTP_400_BAD_REQUEST)

    files = serializer.validated_data['csv_files']
    valid_emails, invalid_emails = CSVEmailParser().parse_csvs(files)
    return Response(data={
        "valid_emails": valid_emails,
        "invalid_emails": invalid_emails,
    }, status=status.HTTP_200_OK)
