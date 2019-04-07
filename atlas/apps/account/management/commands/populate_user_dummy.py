import csv
import json

from django.core.management.base import BaseCommand, CommandError
from atlas.apps.account import models

user_fields = ['email', 'first_name', 'last_name', 'is_verified']
profile_fields = ['gender', 'residence_lng', 'residence_lat', 'latest_csui_class_year',
                  'latest_csui_program', 'birthdate', 'latest_csui_graduation_status']


class Command(BaseCommand):
    help = 'Populate DB with user dummy'

    def handle(self, *args, **options):
        total = 0
        with open('./data/users_dummy.csv', 'r', newline='') as csvfile:
            user_data = csv.DictReader(csvfile)
            for row in user_data:
                raw_user = {}
                for f in user_fields:
                    if f == 'is_verified':
                        row[f] = json.loads(row[f])
                    raw_user[f] = row[f]

                user, created = models.User.objects.get_or_create(
                    email=raw_user.pop('email'), defaults=raw_user)
                if created:
                    for f in profile_fields:
                        setattr(user.profile, f, row[f])
                    user.profile.save(update_fields=profile_fields)
                    total += 1

        self.stdout.write(self.style.SUCCESS(
            'Successfully create %s dummy users' % total))
