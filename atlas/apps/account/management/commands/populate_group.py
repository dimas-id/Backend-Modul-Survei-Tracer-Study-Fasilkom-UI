import csv
import json

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from atlas.apps.account import models


class Command(BaseCommand):
    help = 'Populate group'

    def handle(self, *args, **options):
        total = 0
        groups = [
            'manajemen',
            'admin_donasi',
            'admin_channel',
            'admin_user',
        ]

        for g in groups:
            _, created = Group.objects.get_or_create(name=g)
            if created:
                total += 1
                self.stdout.write(self.style.SUCCESS(f'Group {g} created'))

        self.stdout.write(self.style.SUCCESS(
            'Successfully create %s groups' % total))
