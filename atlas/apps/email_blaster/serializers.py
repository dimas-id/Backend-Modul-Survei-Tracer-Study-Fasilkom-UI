from rest_framework import serializers

from atlas.apps.email_blaster.models import EmailTemplate
from atlas.apps.email_blaster.services import EmailTemplateService
from atlas.apps.survei.services import SurveiService


class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = ('id', 'title', 'email_subject', 'email_body')


class EmailSendRequestSerializer(serializers.Serializer):
    email_template_id = serializers.IntegerField()
    survei_id = serializers.IntegerField()
    recipients = serializers.ListField(child=serializers.EmailField())
    wait_delay = serializers.IntegerField(
        default=10, required=False, min_value=0, max_value=1800)
    batch_size = serializers.IntegerField(
        default=30, required=False, min_value=1, max_value=70)

    def validate_email_template_id(self, value):
        service = EmailTemplateService()
        if service.get_email_template(value) == None:
            raise serializers.ValidationError(
                "Email template with id {} does not exist".format(value))
        return value

    def validate_survei_id(self, value):
        service = SurveiService()
        if service.get_survei(value) == None:
            raise serializers.ValidationError(
                "Survei with id {} does not exist".format(value))
        return value
