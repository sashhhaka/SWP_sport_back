from django.db import models
import datetime
from django.utils import timezone
from django.conf import settings
import uuid
from django.core.exceptions import ValidationError


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
    # subscribed_students = models.ManyToManyField('AchStudent', through='CurrentAchievementAchStudent', blank=True)
    # finished_students = models.ManyToManyField('AchStudent', through='FinishedAchievementAchStudent', blank=True,
    #                                            related_name='finished_students')

    students = models.ManyToManyField('AchStudent', through='AchievementAchStudent', blank=True, related_name='students')

    def __str__(self):
        return self.title

    def get_id(self):
        return self.title + 'id'

    def subscribed_students(self):
        return self.students.filter(achievementachstudent__status='subscribed')

    def finished_students(self):
        return self.students.filter(achievementachstudent__status='finished')

    # function to mark a subcribed student as finished
    def mark_student_as_finished(self, student):
        # check if student is subscribed
        if self.students.filter(achievementachstudent__status='subscribed').filter(id=student.id).exists():
            # get the student
            ach_student = AchievementAchStudent.objects.get(achievement=self, ach_student=student, status='subscribed')
            # mark as finished
            ach_student.status = 'finished'
            ach_student.save()
    def mark_student_as_subscribed(self, student):
        # check if student is subscribed
        if self.students.filter(achievementachstudent__status='finished').filter(id=student.id).exists():
            # get the student
            ach_student = AchievementAchStudent.objects.get(achievement=self, ach_student=student, status='finished')
            # mark as finished
            ach_student.status = 'subscribed'
            ach_student.save()






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
    date_assigned = models.DateField(default=datetime.date.today, blank=False, null=False)

    def __str__(self):
        return ""

    class Meta:
        verbose_name = 'Assigned Achievement'
        verbose_name_plural = 'Assigned Achievements'



class AchievementAchStudent(models.Model):
    ACHIEVEMENT_STATUS_CHOICES = [
        ('subscribed', 'Subscribed'),
        ('finished', 'Finished'),
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
        return ""

    def save(self, *args, **kwargs):
        if self.status != 'finished':
            self.date_achieved = None
        super().save(*args, **kwargs)

    def is_achieved(self):
        return self.status == 'finished'



    is_achieved.boolean = True
    is_achieved.short_description = 'Achieved'

    def clean(self):
        if self.status == 'finished' and not self.date_achieved:
            raise ValidationError({'date_achieved': 'This field is required for finished achievements.'})





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


