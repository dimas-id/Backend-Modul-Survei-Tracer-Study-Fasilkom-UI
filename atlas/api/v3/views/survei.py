from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from atlas.apps.survei.serializers import SurveiSerialize, RadioButtonRequestSerializer
from atlas.apps.survei.services import SurveiService


@api_view()
@permission_classes([IsAuthenticated, IsAdminUser])
def get_list_survei(_):
    survei_service = SurveiService()

    all_list = SurveiSerialize(survei_service.list_survei(), many=True)
    sent_list = SurveiSerialize(survei_service.list_survei_sent(), many=True)
    not_sent_list = SurveiSerialize(survei_service.list_survei_not_sent(), many=True)
    
    response_data = {'survei': all_list.data, 'survei_dikirim': sent_list.data, 'survei_belum_dikirim': not_sent_list.data}
    return Response(data=response_data, status=status.HTTP_200_OK)


@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def register_survei(request):

    serializer = SurveiSerialize(
        data=request.data, context={'request': request})

    if serializer.is_valid():
        survei = serializer.save()

        return Response(data={
            'survei': SurveiSerialize(survei).data},
            status=status.HTTP_201_CREATED)
    else:
        return Response(data={'messages': serializer._errors},
                        status=status.HTTP_400_BAD_REQUEST)