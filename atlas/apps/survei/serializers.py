from rest_framework import serializers
from atlas.apps.survei.services import SurveiService


class SurveiSerialize(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nama = serializers.CharField(max_length=150)
    deskripsi = serializers.CharField(max_length=1200)
    tanggal_dikirim = serializers.DateTimeField(required=False)
    sudah_dikirim = serializers.BooleanField(required=False)

    # create new survei
    def create(self, validated_data):
        request = self.context.get('request')
        survei_service = SurveiService()
        try :   
            survei = survei_service.register_suvei(request, **validated_data)
            return survei
        except:
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