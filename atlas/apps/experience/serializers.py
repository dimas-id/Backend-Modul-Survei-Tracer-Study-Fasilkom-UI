from rest_framework import serializers 
from rest_framework.validators import UniqueValidator

from atlas.apps.experience.models import Education, Position, OtherEducation


class PositionSerializer(serializers.ModelSerializer):

    location_name = serializers.CharField(required=True)
    is_current = serializers.BooleanField(required=False)

    class Meta:
        model = Position
        fields = '__all__'
        read_only_fields = ('user', 'company_metadata', 'is_current')

class PositionTitleSerializer(serializers.ModelSerializer):

    is_current = serializers.BooleanField(required=False)
    
    class Meta:
        model = Position
        fields = ('title','is_current', 'company_name')


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

class ClassAndProgramSerializer(serializers.ModelSerializer):

    class Meta:
        model = Education
        fields = ('csui_class_year', 'csui_program', 'csui_graduation_year', 'csui_graduation_term')
        list_serializer_class = EducationListSerializer

# Create bulk create for other education endpoint
class OtherEducationListSerializer(serializers.ListSerializer):

    def create(self, validated_data):
        other_educations = [OtherEducation(**item) for item in validated_data]
        return OtherEducation.objects.bulk_create(other_educations)

class OtherEducationSerializer(serializers.ModelSerializer):

    class Meta:
        model = OtherEducation
        fields = '__all__'
        read_only_fields = ('user',)
        list_serializer_class = OtherEducationListSerializer
