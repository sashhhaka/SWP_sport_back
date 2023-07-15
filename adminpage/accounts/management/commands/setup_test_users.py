import random
from django.db import transaction
from django.core.management.base import BaseCommand

from accounts.factories import UserFactory
from accounts.models import User

NUM_USERS = 1000


class Command(BaseCommand):
    help = 'Generates test data for achievements application'

    def handle(self, *args, **options):
        # delete all users except admin@innopolis.university, sport@innopolis,university
        # and t.testovich@innopolis.university
        model = User
        for obj in model.objects.all():
            if obj.email not in ['admin@innopolis.university', 'sport@innopolis.university',
                                 't.testovich@innopolis.university']:
                obj.delete()

        # Generate and save the user objects
        with transaction.atomic():
            for _ in range(NUM_USERS):
                UserFactory()
        self.stdout.write(self.style.SUCCESS(f'Generated {NUM_USERS} users'))

        # add 3/4 of users to student group
        users = User.objects.all()
        users = users.exclude(email__in=['admin@innopolis.university', 'sport@innopolis.university',
                                         't.testovich@innopolis.university'])
        count = 0
        for user in users:
            if random.random() < 0.7:
                user.groups.add(1)
                user.save()
                count += 1
        self.stdout.write(self.style.SUCCESS(f'Added {count} of users to student group'))

        # add 1/4 of users to trainer group
        users = User.objects.all()
        users = users.exclude(email__in=['admin@innopolis.university', 'sport@innopolis.university',
                                         't.testovich@innopolis.university'])
        count = 0
        for user in users:
            if random.random() < 0.3:
                user.groups.add(2)
                user.save()
                count += 1
        self.stdout.write(self.style.SUCCESS(f'Added {count} of users to trainer group'))
