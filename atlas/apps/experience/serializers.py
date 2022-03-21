from rest_framework import serializers 
from rest_framework.validators import UniqueValidator

from atlas.apps.experience.models import Education, Position


class PositionSerializer(serializers.ModelSerializer):

    location_name = serializers.CharField(required=True)
    is_current = serializers.BooleanField(required=False)

    class Meta:
        model = Position
        fields = '__all__'
        read_only_fields = ('user', 'company_metadata', 'is_current')

# class PositionTitleSerializer(serializers.ModelSerializer):

#     is_current = serializers.BooleanField(required=False)
    
#     class Meta:
#         model = Position
#         fields = ('title','is_current')


# Create bulk create for education endpoint
class EducationListSerializer(serializers.ListSerializer):

    ui_sso_npm = serializers.CharField(max_length=10,
                                       required=False,
                                       validators=[UniqueValidator(queryset=Education.objects.filter(is_verified=True))])

    def create(self, validated_data):
        educations = [Education(**item) for item in validated_data]
        return Education.objects.bulk_create(educations)


class EducationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Education
        fields = '__all__'
        read_only_fields = ('user',)
        list_serializer_class = EducationListSerializer

# class ClassAndProgramSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Education
#         fields = ('csui_class_year', 'csui_program')
#         list_serializer_class = EducationListSerializer
