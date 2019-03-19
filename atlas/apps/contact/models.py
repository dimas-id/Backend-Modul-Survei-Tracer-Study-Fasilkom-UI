from django.db import models

from atlas.apps.account.models import User

class Contact(User):
    class Meta:
        proxy = True

    @property
    def birthdate(self):
        return self.profile.birthdate

    @property
    def profile_pic_url(self):
        """
        Error AWS
        """
        return self.profile.profile_pic_url

    @property
    def phone_number(self):
        return self.profile.phone_number
    
    @property
    def gender(self):
        return self.profile.gender

    @property
    def residence_city(self):
        return self.profile.residence_city

    @property
    def residence_country(self):
        return self.profile.residence_country

    @property
    def latest_csui_class_year(self):
        return self.profile.latest_csui_class_year

    @property
    def latest_csui_program(self):
        return self.profile.latest_csui_program

    @property
    def website_url(self):
        return self.profile.website_url