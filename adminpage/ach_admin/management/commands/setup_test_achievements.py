import random
from django.db import transaction
from django.core.management.base import BaseCommand



NUM_USERS = 8


class Command(BaseCommand):
    help = 'Generates test data for achievements'

    def handle(self, *args, **options):

        # generate 10 achievements
        from ach_admin.models import Achievement
        # delete all achievements
        model = Achievement
        for obj in model.objects.all():
            obj.delete()


        # set a dictionary of achievement names, short descriptions and icons from static/icons
        achievement_names = ['First achievement', 'Second achievement', 'Third achievement', 'Fourth achievement',
                                'Fifth achievement', 'Sixth achievement', 'Seventh achievement', 'Eighth achievement',
                                'Ninth achievement', 'Tenth achievement']
        achievement_descriptions = ['First achievement description', 'Second achievement description',
                                    'Third achievement description', 'Fourth achievement description',
                                    'Fifth achievement description', 'Sixth achievement description',
                                    'Seventh achievement description', 'Eighth achievement description',
                                    'Ninth achievement description', 'Tenth achievement description']

        # upload icons from static/icons into the database
        achievement_icons = 'achievement.png'

        # generate and save the achievement objects
        with transaction.atomic():
            for i in range(len(achievement_names)):
                Achievement.objects.create(title=achievement_names[i], short_description=achievement_descriptions[i],
                                           icon=achievement_icons)
        self.stdout.write(self.style.SUCCESS(f'Generated {len(achievement_names)} achievements'))
        import datetime
        # assign 8 achievements to admin@innopolis.university AchTeacher
        from ach_admin.models import AchTeacher, AchievementAchTeacher
        from accounts.models import User
        admin = User.objects.get(email='admin@innopolis.university')
        admin_teacher = AchTeacher.objects.get(user=admin)
        achievements = Achievement.objects.all()
        count = 0

        for achievement in achievements:
            if random.random() < 0.8:
                AchievementAchTeacher.objects.create(achievement=achievement, ach_teacher=admin_teacher, date_assigned=datetime.datetime.now())
                count += 1

        # for achievement in achievements:
        #     if random.random() < 0.8:
        #         admin_teacher.achievements.add(achievement)
        #         admin_teacher.save()
        #         count += 1
        # self.stdout.write(self.style.SUCCESS(f'Added {count} of achievements to admin@innopolis.university AchTeacher'))

        # assign half the students as subscribed to the first achievement
        from ach_admin.models import AchStudent, AchievementAchStudent
        from accounts.models import User
        import datetime

        students = AchStudent.objects.all()
        achievement = Achievement.objects.get(title='First achievement')

        count = 0
        for student in students:
            if count < len(students)/2:
                AchievementAchStudent.objects.create(achievement=achievement, ach_student=student, status='subscribed')
                count += 1
            else:
                AchievementAchStudent.objects.create(achievement=achievement, ach_student=student, status='finished',
                                                     date_achieved=datetime.date.today())
                count += 1






