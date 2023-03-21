from rest_framework import serializers
from atlas.apps.survei.models import JENIS_PERTANYAAN
from atlas.apps.survei.services import SurveiService



class SurveiSerialize(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nama = serializers.CharField(max_length=150)
    deskripsi = serializers.CharField(max_length=1200)
    tanggal_dikirim = serializers.DateTimeField(required=False)
    sudah_dikirim = serializers.BooleanField(required=False)
    tanggal_dibuat = serializers.DateTimeField(required=False)
    tanggal_diedit = serializers.DateTimeField(required=False)
    creator = serializers.CharField(max_length=150, required=False)

    # create new survei
    def create(self, validated_data):
        request = self.context.get('request')
        survei_service = SurveiService()

        try:
            survei = survei_service.register_suvei(request, **validated_data)
            return survei
        except TypeError:
            return None

    # update existing survei

    def update(self, instance, validated_data):
        instance.nama = validated_data.get('nama', instance.nama)
        instance.deskripsi = validated_data.get(
            'deskripsi', instance.deskripsi)
        instance.tanggal_dikirim = validated_data.get(
            'tanggal_dikirim', instance.tanggal_dikirim)
        instance.sudah_dikirim = validated_data.get(
            'sudah_dikirim', instance.sudah_dikirim)
        instance.save()
        return instance
    

class PertanyaanSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    pertanyaan = serializers.CharField(max_length=1200)
    jenis_jawaban = serializers.ChoiceField(choices=JENIS_PERTANYAAN)
    wajib_diisi = serializers.BooleanField()


class OpsiJawabanSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    opsi_jawaban = serializers.CharField(max_length=150)

    
class IsianRequestSerializer(serializers.Serializer):
    survei_id = serializers.IntegerField(required=True)
    pertanyaan = serializers.CharField(max_length=1200)
    wajib_diisi = serializers.BooleanField(required=False)
    jawaban = serializers.CharField(max_length=150, required=False)

    def validate_survei_id(self, value):
        survei_service = SurveiService()
        try:
            survei = survei_service.get_survei(value)
            if survei is None:
                raise serializers.ValidationError(
                    "Survei dengan id {} tidak ditemukan".format(value))
            return value
        except:
            raise serializers.ValidationError(
                "Survei dengan id {} tidak ditemukan".format(value))

    def create(self, validated_data):
        survei_id = validated_data.get('survei_id')
        pertanyaan = validated_data.get('pertanyaan')
        wajib_diisi = validated_data.get('wajib_diisi')
        survei_service = SurveiService()
        try:
            survei = survei_service.get_survei(survei_id)
            pertanyaan = survei_service.register_pertanyaan_isian(survei=survei, pertanyaan=pertanyaan, wajib_diisi=wajib_diisi)
            jawaban_isian_singkat = survei_service.register_opsi_jawaban_isian(pertanyaan=pertanyaan, isian="")
            return {"pertanyaan": pertanyaan, "jawaban_isian_singkat": jawaban_isian_singkat}
        except:
            return None

class SkalaLinierRequestSerializer(serializers.Serializer):
    survei_id = serializers.IntegerField(required=True)
    pertanyaan = serializers.CharField(required=True)
    pertanyaan_wajib_diisi = serializers.BooleanField(
        required=False, default=False)
    banyak_skala = serializers.IntegerField(
        required=False, default=5, min_value=2, max_value=15)
    mulai_dari_satu = serializers.BooleanField(required=False, default=False)

    def validate_survei_id(self, value):
        """Check if survei with survei_id exists"""
        survei_service = SurveiService()
        if survei_service.get_survei(value) == None:
            raise serializers.ValidationError(
                "Survei with id {} does not exist".format(value))
        return value

    def create(self, validated_data):
        """Create pertanyaan dan skala linier objects"""
        survei_service = SurveiService()

        survei_obj = survei_service.get_survei(validated_data.get('survei_id'))

        pertanyaan_obj = survei_service.register_pertanyaan_skala_linier(
            survei=survei_obj,
            pertanyaan=validated_data.get("pertanyaan"),
            wajib_diisi=validated_data.get("pertanyaan_wajib_diisi"))

        skala_linier_objs = []
        banyak_skala = validated_data.get('banyak_skala')
        mulai_dari_satu = validated_data.get('mulai_dari_satu')
        for i in range(mulai_dari_satu, banyak_skala+mulai_dari_satu):
            skala_linier_objs.append(survei_service.register_opsi_jawaban_skala_linier(
                pertanyaan=pertanyaan_obj, skala=i))

        return {"pertanyaan": pertanyaan_obj, "skala_linier": skala_linier_objs}