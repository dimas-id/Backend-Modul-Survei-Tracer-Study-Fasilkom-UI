from django.forms import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from atlas.apps.survei.serializers import OpsiJawabanSerializer, PertanyaanCreateRequestSerializer, PertanyaanSerializer, SurveiCreateRequestSerializer, SurveiSerializer
from atlas.apps.survei.services import SurveiService


@api_view()
@permission_classes([IsAuthenticated, IsAdminUser])
def get_list_survei(_):
    survei_service = SurveiService()

    all_list = SurveiSerializer(survei_service.list_survei(), many=True)
    sent_list = SurveiSerializer(survei_service.list_survei_sent(), many=True)
    not_sent_list = SurveiSerializer(
        survei_service.list_survei_not_sent(), many=True)

    response_data = {'survei': all_list.data, 'survei_dikirim': sent_list.data,
                     'survei_belum_dikirim': not_sent_list.data}
    return Response(data=response_data, status=status.HTTP_200_OK)


@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def register_survei(request):
    survei_request_serializer = SurveiCreateRequestSerializer(
        data=request.data, context={'request': request})

    if not survei_request_serializer.is_valid():
        return Response(data={'messages': survei_request_serializer._errors},
                        status=status.HTTP_400_BAD_REQUEST)

    survei = survei_request_serializer.save()

    pertanyaan_list_data = survei_request_serializer.validated_data.get(
        'pertanyaan') or []

    errors = []
    serialized_pertanyaan_list = []

    for i, pertanyaan_data in enumerate(pertanyaan_list_data):

        if not isinstance(pertanyaan_data, dict):
            errors.append(f"Data pertanyaan ke-{i+1} tidak valid")
            continue

        pertanyaan_serializer = PertanyaanCreateRequestSerializer(
            data={**pertanyaan_data, 'survei_id': survei.id})
        try:
            if not pertanyaan_serializer.is_valid():
                raise ValidationError(pertanyaan_serializer._errors)
            pertanyaan_objects = pertanyaan_serializer.save()
            serialized_pertanyaan_list.append({
                'pertanyaan': PertanyaanSerializer(
                    pertanyaan_objects.get('pertanyaan')).data,
                'opsi_jawaban': OpsiJawabanSerializer(
                    pertanyaan_objects.get('opsi_jawaban'), many=True).data})
        except ValidationError as e:
            errors.append(f"Pertanyaan ke-{i+1} error: {e}")

    return Response(data={
        'survei': SurveiSerializer(survei).data,
        'pertanyaan': serialized_pertanyaan_list,
        'errors': errors},
        status=status.HTTP_201_CREATED)
