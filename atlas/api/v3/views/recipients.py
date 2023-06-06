from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from atlas.apps.email_blaster.serializers import CSVFilesSerializer, EmailRecipientSerializer
from atlas.apps.email_blaster.services import CSVEmailParser, EmailRecipientService


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


@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_email_recipients(request):

    """Fetch all of the email recipients as requested"""

    serializer = EmailRecipientSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(data={'messages': serializer._errors},
                        status=status.HTTP_400_BAD_REQUEST)
    
    email_recipient_object = serializer.save()

    return Response(
            data={"recipients" : email_recipient_object.get("emails")},
            status=status.HTTP_201_CREATED)


@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_total_recipients_of_group_email(request):

    """Get total number recipients from a group of alumni
    and also get the total number of alumni that havent filled the survey"""

    data = request.data

    email_recipient_service = EmailRecipientService()

    try :
        alumni_emails = email_recipient_service.get_all_student_by_graduation_year_and_term(data["year"], data["term"])
        total_alumni_non_response = email_recipient_service.get_total_alumni_of_a_group_that_havent_filled_survey(alumni_emails, data["survei_id"])

        return Response(
            data={"total_all": len(alumni_emails), 
                  "total_non_response": total_alumni_non_response},
            status=status.HTTP_200_OK)
    
    except Exception as error:
        return Response(
            data={'messages': error},
            status=status.HTTP_400_BAD_REQUEST)