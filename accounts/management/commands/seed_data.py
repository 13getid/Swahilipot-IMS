from django.core.management.base import BaseCommand

from accounts.models import User
from core.models import Department

DEPARTMENTS = [
    ('Communication', 'communication', True, True),
    ('Creatives', 'creatives', True, False),
    ('Tech Department', 'tech', True, False),
    ('Community Experience', 'community-experience', True, False),
    ('Youth Engagement', 'youth-engagement', True, False),
    ('Heritage', 'heritage', True, False),
    ('Admin', 'admin', False, False),
    ('Finance', 'finance', False, False),
    ('Entrepreneurship', 'entrepreneurship', True, False),
]

DEFAULT_PASSWORD = 'Swahilipot@2024'


class Command(BaseCommand):
    help = 'Creates the 9 departments and a default supervisor + instructor for each.'

    def handle(self, *args, **options):
        for name, slug, has_trainees, has_radio in DEPARTMENTS:
            dept, created = Department.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': name,
                    'has_trainees': has_trainees,
                    'has_radio_report': has_radio,
                },
            )
            self.stdout.write(f"{'Created' if created else 'Exists '} department: {name}")

            for role in ('supervisor', 'instructor'):
                email = f'{role}.{slug}@swahilipothub.co.ke'
                if not User.objects.filter(email=email).exists():
                    User.objects.create_user(
                        email=email,
                        password=DEFAULT_PASSWORD,
                        name=f'{name} {role.title()}',
                        role=role,
                        department=dept,
                    )
                    self.stdout.write(f'  Created {role}: {email}')

        self.stdout.write(self.style.SUCCESS('Seeding complete.'))