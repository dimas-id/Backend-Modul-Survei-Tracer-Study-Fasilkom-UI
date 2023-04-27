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

@api_view()
@permission_classes([IsAuthenticated])
def get_survei_by_id(request):
    survei_id = request.query_params.get('survei_id')
    survei_service = SurveiService()
    
    survei = survei_service.get_survei(survei_id)
    if survei == None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serialized_survei = SurveiSerializer(survei).data
    list_pertanyaan = PertanyaanSerializer(survei_service.get_list_pertanyaan_by_survei_id(survei_id), many=True).data
    list_opsi_jawaban = OpsiJawabanSerializer(survei_service.get_list_opsi_jawaban(survei_id), many=True).data
    response_data = {'survei': serialized_survei, 'list_pertanyaan': list_pertanyaan, 'list_opsi_jawaban': list_opsi_jawaban}
    
    return Response(data=response_data, status=status.HTTP_200_OK)
    
@api_view(http_method_names=['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_survei_by_id(request):
    survei_id = request.query_params.get('survei_id')
    survei_service = SurveiService()

    survei = survei_service.delete_survei(survei_id)
    if survei[0] == SurveiService.DELETE_NOT_FOUND:
        return Response(status=status.HTTP_404_NOT_FOUND)
    elif survei[0] == SurveiService.DELETE_PUBLISHED:
        return Response(status=status.HTTP_403_FORBIDDEN)
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def register_survei(request):
    survei_request_serializer = SurveiCreateRequestSerializer(
        data=request.data, context={'request': request})

    survei_is_valid = survei_request_serializer.is_valid()

    # Check 'nama','deskripsi','pertanyaan param
    if not survei_is_valid:
        survei_request_serializer = SurveiCreateRequestSerializer(
            data={
                'nama': 'DELETE ME',
                'deskripsi': 'You should not be able to see this',
                'pertanyaan': request.data.get('pertanyaan') or []
            },
            context={'request': request}
        )

    # Check 'pertanyaan' param again
    if not survei_request_serializer.is_valid():
        survei_request_serializer = SurveiCreateRequestSerializer(
            data={
                'nama': 'DELETE ME',
                'deskripsi': 'You should not be able to see this',
                'pertanyaan': []
            },
            context={'request': request}
        )

    survei_request_serializer.is_valid()
    # if survei is not valid, survei will later be deleted
    survei = survei_request_serializer.save()

    pertanyaan_list_data = survei_request_serializer.validated_data.get(
        'pertanyaan')
    success_matrix = []
    valid_pertanyaan_list = []

    for pertanyaan_data in pertanyaan_list_data:

        if not isinstance(pertanyaan_data, dict):
            success_matrix.append(False)
            continue

        pertanyaan_serializer = PertanyaanCreateRequestSerializer(
            data={**pertanyaan_data, 'survei_id': survei.id})
        if not pertanyaan_serializer.is_valid():
            success_matrix.append(False)
            continue

        success_matrix.append(True)
        valid_pertanyaan_list.append(pertanyaan_serializer)

    if not survei_is_valid or (False in success_matrix):
        survei.delete()
        return Response(data={
            'status': 'failed',
            'messages': success_matrix,
        }, status=status.HTTP_400_BAD_REQUEST)
    serialized_pertanyaan_list = []
    for pertanyaan in valid_pertanyaan_list:
        pertanyaan_obj = pertanyaan.save()
        serialized_pertanyaan_list.append({
            'pertanyaan': PertanyaanSerializer(
                pertanyaan_obj.get('pertanyaan')).data,
            'opsi_jawaban': OpsiJawabanSerializer(
                pertanyaan_obj.get('opsi_jawaban'), many=True).data})

    return Response(data={
        'survei': SurveiSerializer(survei).data,
        'pertanyaan': serialized_pertanyaan_list},
        status=status.HTTP_201_CREATED)


@api_view(http_method_names=['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
def edit_survei_by_id(request):
    try:
        survei_id = request.query_params.get('survei_id')
        survei_service = SurveiService()
        survei = survei_service.get_survei(survei_id)
    except survei.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    survei_request_serializer = SurveiCreateRequestSerializer(
        survei, data=request.data, context={'request': request}, partial=True
    )

    survei_is_valid = survei_request_serializer.is_valid()

    # Check 'nama','deskripsi','pertanyaan param
    if not survei_is_valid:
        survei_request_serializer = SurveiCreateRequestSerializer(
            data={
                'nama': 'DELETE ME',
                'deskripsi': 'You should not be able to see this',
                'pertanyaan': request.data.get('pertanyaan') or []
            },
            context={'request': request}
        )

                # Check 'pertanyaan' param again
    if not survei_request_serializer.is_valid():
        survei_request_serializer = SurveiCreateRequestSerializer(
            data={
                'nama': 'DELETE ME',
                'deskripsi': 'You should not be able to see this',
                'pertanyaan': []
            },
            context={'request': request}
        )
    
    survei_request_serializer.is_valid()
    survei = survei_request_serializer.save()

    pertanyaan_list_data = survei_request_serializer.validated_data.get(
        'pertanyaan')
    success_matrix = []
    valid_pertanyaan_list = []

    for pertanyaan_data in pertanyaan_list_data:

        if not isinstance(pertanyaan_data, dict):
            success_matrix.append(False)
            continue

        pertanyaan_serializer = PertanyaanCreateRequestSerializer(
            data={**pertanyaan_data, 'survei_id': survei.id}
        )
        if not pertanyaan_serializer.is_valid():
            success_matrix.append(False)
            break

        success_matrix.append(True)
        valid_pertanyaan_list.append(pertanyaan_serializer)

    if not survei_is_valid or (False in success_matrix):
        survei.delete()
        return Response(
            data={
                'status': 'failed',
                'messages': success_matrix,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    serialized_pertanyaan_list = []
    for pertanyaan in valid_pertanyaan_list:
        pertanyaan_obj = pertanyaan.save()
        serialized_pertanyaan_list.append(
            {
                'pertanyaan': PertanyaanSerializer(
                    pertanyaan_obj.get('pertanyaan')
                ).data,
                'opsi_jawaban': OpsiJawabanSerializer(
                    pertanyaan_obj.get('opsi_jawaban'), many=True
                ).data,
            }
        )

    return Response(
        data={
            'survei': SurveiSerializer(survei).data,
            'pertanyaan': serialized_pertanyaan_list,
        },
        status=status.HTTP_200_OK,
    )
