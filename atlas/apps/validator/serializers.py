from django.utils import timezone
from rest_framework import serializers

MIN_GENERATION = 1986


class AlumniValidationSerializer(serializers.Serializer):
    nama = serializers.CharField(required=False)
    npm = serializers.CharField(required=False)
    nm_org = serializers.CharField(required=False)
    angkatan = serializers.IntegerField(
        required=False, min_value=MIN_GENERATION, max_value=timezone.now().year)
    status_terakhir_mhs = serializers.CharField(read_only=True)

    kota_lahir = serializers.CharField(read_only=True)
    tgl_lahir = serializers.DateField(required=False)
    alamat = serializers.CharField(read_only=True)

    is_valid = serializers.BooleanField(read_only=True)

    def validate(self, attrs):
        nama = attrs.get('nama', None)
        npm = attrs.get('npm', None)

        if not npm and not nama:
            raise serializers.ValidationError('Identifier needed: npm or nama')

        return attrs

    def validate_npm(self, value):
        if not f'{value}'.isdigit():
            raise serializers.ValidationError('npm is not digit.')
        return value
