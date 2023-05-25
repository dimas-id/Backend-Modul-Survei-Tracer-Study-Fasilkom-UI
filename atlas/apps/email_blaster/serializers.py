from rest_framework import serializers
import csv
from atlas.apps.email_blaster.models import EmailTemplate
from atlas.apps.email_blaster.services import EmailTemplateService, EmailRecipientService
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

class CSVFilesSerializer(serializers.Serializer):
    """Serializer for CSV files
    """

    csv_files = serializers.ListField(child=serializers.FileField())

    def validate_csv_files(self, value):
        if not value:
            raise serializers.ValidationError(
                "At least one CSV file is required.")

        for file in value:
            if not file.name.endswith('.csv'):
                raise serializers.ValidationError(
                    f"File '{file.name}' is not a CSV file.")

        return value


class EmailRecipientSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    survei_id = serializers.IntegerField(required=True)
    group_recipients_years = serializers.ListField(
        child=serializers.IntegerField(required=False),
        allow_empty=True)
    group_recipients_terms = serializers.ListField(
        child=serializers.IntegerField(required=False),
        allow_empty=True)
    individual_recipients_emails = serializers.ListField(
        child=serializers.CharField(required=False, max_length=100),
        allow_empty=True)
    csv_emails = serializers.ListField(
        child=serializers.CharField(required=False, max_length=100),
        allow_empty=True)

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
        survei_service = SurveiService()
        email_recipient_service = EmailRecipientService()

        survei_obj = survei_service.get_survei(validated_data.get('survei_id'))

        email_recipient_data = email_recipient_service.create_email_recipient_data(
            survei=survei_obj,
            group_recipients_years=validated_data.get("group_recipients_years"),
            group_recipients_terms=validated_data.get("group_recipients_terms"),
            individual_recipients_emails=validated_data.get("individual_recipients_emails"),
            csv_emails=validated_data.get("csv_emails"))
        
        all_emails = email_recipient_service.get_email_recipients(
            email_recipient_data.group_recipients_years,
            email_recipient_data.group_recipients_terms,
            email_recipient_data.individual_recipients_emails,
            email_recipient_data.csv_emails)
        
        all_emails = email_recipient_service.exclude_alumni_that_has_responded(all_emails, validated_data.get('survei_id'))
        
        return {
            "emails" : all_emails
        }
