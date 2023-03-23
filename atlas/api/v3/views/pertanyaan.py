from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from atlas.apps.survei.serializers import OpsiJawabanSerializer, PertanyaanSerializer, SkalaLinierRequestSerializer, IsianRequestSerializer, RadioButtonRequestSerializer, DropDownRequestSerializer, CheckBoxRequestSerializer


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

@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def register_isian(request):
    serializer = IsianRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(data={'messages': serializer._errors},
                        status=status.HTTP_400_BAD_REQUEST)
    objects = serializer.save()

    pertanyaan = objects.get("pertanyaan")
    isian = objects.get("jawaban_isian_singkat")

    return Response(data={
        'pertanyaan': PertanyaanSerializer(pertanyaan).data,
        'jawaban_isian_singkat': OpsiJawabanSerializer(isian).data},
        status=status.HTTP_201_CREATED)


@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def register_radiobutton(request):
    """Registering Radio Button Questions via API"""

    serializer = RadioButtonRequestSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(data={'messages': serializer._errors},
                        status=status.HTTP_400_BAD_REQUEST)
    objects = serializer.save()

    pertanyaan = objects.get("pertanyaan")
    opsi_jawaban = objects.get("opsi_jawaban")

    pertanyaan_obj = PertanyaanSerializer(pertanyaan).data
    opsi_jawaban_obj = OpsiJawabanSerializer(opsi_jawaban, many=True).data

    return Response(data={
        'pertanyaan': pertanyaan_obj,
        'opsi_jawaban': opsi_jawaban_obj},
        status=status.HTTP_201_CREATED)

@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def register_dropdown(request):
    """Registering Drop Down Questions via API"""

    serializer = DropDownRequestSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(data={'messages': serializer._errors},
                        status=status.HTTP_400_BAD_REQUEST)
    objects = serializer.save()

    pertanyaan = objects.get("pertanyaan")
    opsi_jawaban = objects.get("opsi_jawaban")

    pertanyaan_obj = PertanyaanSerializer(pertanyaan).data
    opsi_jawaban_obj = OpsiJawabanSerializer(opsi_jawaban, many=True).data

    return Response(data={
        'pertanyaan': pertanyaan_obj,
        'opsi_jawaban': opsi_jawaban_obj},
        status=status.HTTP_201_CREATED)


@api_view(http_method_names=['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def register_checkbox(request):
    """Registering Checkbox Questions via API"""
    serializer = CheckBoxRequestSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(data={'messages': serializer._errors},
                        status=status.HTTP_400_BAD_REQUEST)
    objects = serializer.save()

    pertanyaan = objects.get("pertanyaan")
    opsi_jawaban = objects.get("opsi_jawaban")

    pertanyaan_obj = PertanyaanSerializer(pertanyaan).data
    opsi_jawaban_obj = OpsiJawabanSerializer(opsi_jawaban, many=True).data

    return Response(data={
        'pertanyaan': pertanyaan_obj,
        'opsi_jawaban': opsi_jawaban_obj},
        status=status.HTTP_201_CREATED)