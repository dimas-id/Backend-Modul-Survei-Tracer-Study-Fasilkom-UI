from datetime import date
from .models import Position


class ExperienceService:

    def extract_and_create_positions_from_linkedin(self, user, positions):
        list_pos = []

        # linkedin is not providing day
        def transform_date(dict_date): return date(
            dict_date['year'], dict_date['month'], 1)

        for pos in positions:
            location = pos['location'].get('name')

            date_ended = None
            if not pos['is_current']:
                date_ended = transform_date(pos['end_date'])

            date_started = transform_date(pos['start_date'])
            new_pos = Position.objects.create(
                user=user,
                title=pos['title'],
                company_name=pos['company']['name'],
                industry_name=pos['company']['industry'],
                location_name=location,
                date_ended=date_ended,
                date_started=date_started,
                company_metadata=pos['company'])

            list_pos.append(new_pos)

        return list_pos
