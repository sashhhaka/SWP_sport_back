from django.db import models
import datetime
from django.utils import timezone
from django.conf import settings
import uuid


# base models

def get_achievement_icon_path(instance, filename):
    ext = filename.split('.')[-1]
    return f'{settings.ACHIEVEMENT_FOLDER}/' \
           f'{instance.title}/{uuid.uuid4()}.{ext}'


# models.py

class Achievement(models.Model):
    title = models.CharField(max_length=200, unique=True, blank=False)
    icon = models.ImageField(upload_to="ach_admin/acheivements", default=None)
    assigned_coaches = models.ManyToManyField('AchTeacher', through='AchievementAchTeacher', blank=True, )
    subscribed_students = models.ManyToManyField('AchStudent', through='CurrentAchievementAchStudent', blank=True)
    finished_students = models.ManyToManyField('AchStudent', through='FinishedAchievementAchStudent', blank=True,
                                               related_name='finished_students')

    def __str__(self):
        return self.title

    def get_id(self):
        return self.title + 'id'


class AchTeacher(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, default=None)
    club_name = models.CharField(max_length=200)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'Teacher with Achievement'
        verbose_name_plural = 'Teacher with Achievements'


class AchStudent(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, default=None, limit_choices_to={
        'groups__verbose_name': settings.STUDENT_AUTH_GROUP_VERBOSE_NAME
    }, )

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'Student with Achievement'
        verbose_name_plural = 'Students with Achievements'


class AchievementAchTeacher(models.Model):
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    ach_teacher = models.ForeignKey(AchTeacher, on_delete=models.CASCADE)
    date_achieved = models.DateField(default=datetime.date.today)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = 'Assigned Achievement'
        verbose_name_plural = 'Assigned Achievements'


class AchievementAchStudent(models.Model):
    ACHIEVEMENT_STATUS_CHOICES = [
        ('subscribed', 'Subscribed'),
        ('finished', 'Finished'),
        ('unsubscribed', 'Unsubscribed'),
    ]

    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    ach_student = models.ForeignKey(AchStudent, on_delete=models.CASCADE)
    date_achieved = models.DateField(default=datetime.date.today, blank=True, null=True)
    status = models.CharField(max_length=20, choices=ACHIEVEMENT_STATUS_CHOICES)

    class Meta:
        verbose_name = 'Achievement Status'
        verbose_name_plural = 'Achievement Statuses'
        constraints = [
            models.UniqueConstraint(
                fields=['ach_student', 'achievement'],
                name='unique_achievement_status'
            )
        ]

    def __str__(self):
        return f"{self.ach_student} - {self.achievement} ({self.status})"

    def save(self, *args, **kwargs):
        if self.status != 'finished':
            self.date_achieved = None
        super().save(*args, **kwargs)

    def is_achieved(self):
        return self.status == 'finished'

    is_achieved.boolean = True
    is_achieved.short_description = 'Achieved'


class CurrentAchievementAchStudent(models.Model):
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    ach_student = models.ForeignKey(AchStudent, on_delete=models.CASCADE)
    date_achieved = models.DateField(default=datetime.date.today)

    class Meta:
        verbose_name = 'Current Achievement'
        verbose_name_plural = 'Current Achievements'

    def __str__(self):
        return ""


class FinishedAchievementAchStudent(models.Model):
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    ach_student = models.ForeignKey(AchStudent, on_delete=models.CASCADE)
    date_achieved = models.DateField(default=datetime.date.today)

    class Meta:
        verbose_name = 'Finished Achievement'
        verbose_name_plural = 'Finished Achievements'

    def __str__(self):
        return ""

"""
Events models
"""


