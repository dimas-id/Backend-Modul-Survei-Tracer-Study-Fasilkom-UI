from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from atlas.apps.survei.serializers import OpsiJawabanSerializer, PertanyaanSerializer, SkalaLinierRequestSerializer


@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def register_skala_linier(request):
    serializer = SkalaLinierRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(data={'messages': serializer._errors},
                        status=status.HTTP_400_BAD_REQUEST)
    objects = serializer.save()

    pertanyaan = objects.get("pertanyaan")
    skala_liniers = objects.get("skala_linier")

    return Response(data={
        'pertanyaan': PertanyaanSerializer(pertanyaan).data,
        'skala_liniers': OpsiJawabanSerializer(skala_liniers, many=True).data},
        status=status.HTTP_201_CREATED)
