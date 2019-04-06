from rest_framework import serializers

from atlas.apps.experience.models import Education, Position


class PositionSerializer(serializers.ModelSerializer):

    location_name = serializers.CharField(required=True)
    is_current = serializers.BooleanField(required=False)

    class Meta:
        model = Position
        fields = '__all__'
        read_only_fields = ('user', 'company_metadata', 'is_current')


class EducationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Education
        fields = '__all__'
        read_only_fields = ('user',)
