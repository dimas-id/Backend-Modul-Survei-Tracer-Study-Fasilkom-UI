from rest_framework import serializers

from atlas.apps.experience.models import Education, Position


class PositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Position
        fields = '__all__'
        read_only_fields = ('user',)


class EducationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Education
        fields = '__all__'
        read_only_fields = ('user',)