from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from atlas.apps.survei.services import SurveiService
from atlas.apps.response.services import ResponseService

@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated])
def isi_survei(request):
    json_data = request.data
    survei_id = json_data["survei_id"]
    user_id = json_data["user_id"]
    jawaban = json_data["jawaban"]
    jawaban_keys_list = list(jawaban.keys())

    survei_service = SurveiService()
    response_service = ResponseService()
    survei = survei_service.get_survei(survei_id)
    list_pertanyaan = survei_service.get_list_pertanyaan_by_survei_id(
        survei_id)
    required_id_list = [obj.id for obj in list_pertanyaan if obj.wajib_diisi]
    
    jawaban_not_valid = response_service.check_jawaban_validity(required_id_list, jawaban_keys_list, jawaban)
    if jawaban_not_valid:
        return Response(data={
            'status': 'failed',
            'messages': jawaban_not_valid,
        }, status=status.HTTP_400_BAD_REQUEST)
            
    
    new_response = response_service.register_response(user_id, survei)
    for pertanyaan in list_pertanyaan:
        id_pertanyaan_str = str(pertanyaan.id)
        if id_pertanyaan_str in (jawaban_keys_list):
            jawaban_col = jawaban[id_pertanyaan_str]
            if isinstance(jawaban_col, list):
                for jaw in jawaban_col:
                    response_service.register_jawaban(pertanyaan, new_response, jaw)
            else:
                response_service.register_jawaban(pertanyaan, new_response, jawaban_col)
    return Response(status=status.HTTP_201_CREATED)