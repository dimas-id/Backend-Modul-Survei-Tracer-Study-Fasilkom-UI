from rest_framework import serializers

from atlas.apps.email_blaster.models import EmailTemplate


class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = ('id', 'title', 'email_subject', 'email_body')
