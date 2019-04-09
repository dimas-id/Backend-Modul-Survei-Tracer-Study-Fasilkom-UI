from django.contrib.auth import get_user_model
from django.db import transaction
from atlas.apps.account.services import UserService
from atlas.apps.experience.services import ExperienceService
from .models import LinkedinAccount


class ExternalAuthService:

    user_service = UserService()

    def connect_user_to_linkedin_account(self, user, **linkedin_user_data):
        linkedin_id = linkedin_user_data.pop("id")
        email_address = linkedin_user_data.pop("email_address")
        linkedin_account, created = LinkedinAccount.objects\
            .get_or_create(id=linkedin_id,
                           user=user,
                           defaults={'email_address': email_address,
                                     'user_data': linkedin_user_data})
        return linkedin_account, created

    @transaction.atomic
    def get_or_register_linkedin_user(self, **linkedin_user_data):
        email_address = linkedin_user_data.get("email_address")
        first_name = linkedin_user_data.get("first_name")
        last_name = linkedin_user_data.get("last_name")
        picture_url = linkedin_user_data.get("picture_url")

        user, created = self.user_service.get_or_register_external_auth_user(
            email_address, first_name, last_name, picture_url)
        _, created_linkedin  = self.connect_user_to_linkedin_account(
            user, **linkedin_user_data)

        '''
        @todo: temporary fix, find elegant solution
        '''
        if created_linkedin and linkedin_user_data.get('positions').get('_total') > 0:
            ExperienceService().extract_and_create_positions_from_linkedin(
                user, linkedin_user_data.get('positions').get('values'))

        return user, created
