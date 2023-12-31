from rest_framework import serializers

from atlas.apps.contact.models import Contact

class ContactSerializer(serializers.ModelSerializer):
    profile_picture_url = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = (
            'id',
            'name',
            'email',
            'ui_sso_npm',
            'gender',
            'phone_number',
            'birthdate',
            'residence_city',
            'residence_country',
            'latest_csui_class_year',
            'latest_csui_program',
            'profile_picture_url',
            'website_url',
        )
        
        read_only_fields = (
            'name',
            'email',
        )

    def get_profile_picture_url(self, instance):
        """
        Error AWS (SOLVED)
        See: https://gitlab.cs.ui.ac.id/propensi-b3/b3-atlas/issues/17
        """
       # method ini harus ada karena kita define attr profile..url di atas,
       # SerializerMethodField udah jago langsung manggil method ini
        return instance.profile_pic_url
