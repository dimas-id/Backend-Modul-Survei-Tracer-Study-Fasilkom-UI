from rest_framework import serializers

from atlas.apps.contact.models import Contact

class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = (
            'id',
            'name',
            'email',
            'gender',
            'phone_number',
            'birthdate',
            'residence_city',
            'residence_country',
            'latest_csui_class_year',
            'latest_csui_program',
        #Error AWS    'profile_pic_url',
            'website_url',
        )
        
        read_only_fields = (
            'name',
            'email',
        )
