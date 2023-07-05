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
    title = models.CharField(max_length=200)
    icon = models.ImageField(upload_to="ach_admin/acheivements", default=None)
    assigned_coaches = models.ManyToManyField('AchTeacher', blank=True, )
    subscribed_students = models.ManyToManyField('AchStudent',  blank=True)
    finished_students = models.ManyToManyField('AchStudent', blank=True,
                                               related_name='finished_students')

    def __str__(self):
        return self.title

    def get_id(self):
        return self.title + 'id'


class AchTeacher(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, default=None)
    club_name = models.CharField(max_length=200)
    is_admin = models.BooleanField(default=False)
    #assigned_achievements = models.ManyToManyField(Achievement, blank=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'Teacher Achievement'
        verbose_name_plural = 'Teacher Achievements'


class AchStudent(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, default=None, limit_choices_to={
            'groups__verbose_name': settings.STUDENT_AUTH_GROUP_VERBOSE_NAME
        },)
    # current_achievements = models.ManyToManyField(Achievement, blank=True, related_name='current_achievements')
    # finished_achievements = models.ManyToManyField(Achievement, blank=True, related_name='finished_achievements')

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'Student Achievement'
        verbose_name_plural = 'Student Achievements'


class AchievementAchTeacher(models.Model):
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    ach_teacher = models.ForeignKey(AchTeacher, on_delete=models.CASCADE)
    date_achieved = models.DateField()

    def __str__(self):
        return f""

    class Meta:
        verbose_name = 'Assigned Achievement'
        verbose_name_plural = 'Assigned Achievements'


class CurrentAchievementAchStudent(models.Model):
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    ach_student = models.ForeignKey(AchStudent, on_delete=models.CASCADE)
    date_achieved = models.DateField()

    class Meta:
        verbose_name = 'Current Achievement'
        verbose_name_plural = 'Current Achievements'

    def __str__(self):
        return f"{self.achievement} - {self.ach_student}"


class FinishedAchievementAchStudent(models.Model):
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    ach_student = models.ForeignKey(AchStudent, on_delete=models.CASCADE)
    date_achieved = models.DateField()

    class Meta:
        verbose_name = 'Finished Achievement'
        verbose_name_plural = 'Finished Achievements'

    def __str__(self):
        return f"{self.achievement} - {self.ach_student}"


# test models
