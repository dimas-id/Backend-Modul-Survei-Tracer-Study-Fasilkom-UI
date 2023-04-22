from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes

from atlas.apps.survei.models import Survei, Pertanyaan
from atlas.apps.response.models import Jawaban, Response as Res
from atlas.apps.survei.serializers import PertanyaanSerializer, SurveiSerializer


@api_view(http_method_names=['GET'])
@permission_classes([IsAdminUser, IsAuthenticated])
def get_visualisasi(req, id):
    try:
        survei = Survei.objects.get(id=id)
        survei_serializer = SurveiSerializer(survei).data
        list_pertanyaan = Pertanyaan.objects.filter(survei=survei)
        list_pertanyaan_serializer = PertanyaanSerializer(
            list_pertanyaan, many=True).data

        for i in range(0, len(list_pertanyaan_serializer)):
            label = []
            data = []
            list_jawaban = Jawaban.objects.filter(
                pertanyaan=list_pertanyaan[i])
            raw_data = {}

            for j in list_jawaban:
                if j.jawaban in raw_data:
                    raw_data[j.jawaban] += 1
                else:
                    raw_data[j.jawaban] = 1

            for key in raw_data:
                label.append(key)
                data.append(raw_data[key])

            list_pertanyaan_serializer[i]["label"] = label
            list_pertanyaan_serializer[i]["data"] = data

        responden = len(Res.objects.filter(survei=survei))

        return Response(data={"survei": survei_serializer, "responden": responden, "pertayaan": list_pertanyaan_serializer}, status=status.HTTP_200_OK)

    except Survei.DoesNotExist:
        return Response(data={"message": "Survei doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
