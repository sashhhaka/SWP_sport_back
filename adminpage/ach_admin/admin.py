from django.contrib import admin
from sport.admin.site import site

admin.site.site_url = 'http://127.0.0.1:8000/ach_admin/'

from .models import Achievement, AchTeacher, AchStudent
from .forms import AchievementForm

"""Inlines for ach_student and ach_teacher
Enable many-to-many relationship in admin page for them
"""


class AchievementSubscribed(admin.TabularInline):
    model = Achievement.subscribed_students.through
    extra = 1

    class Meta:
        verbose_name = "Subscribed student"
        verbose_name_plural = "Subscribed students"


class AchievementFinished(admin.TabularInline):
    model = Achievement.finished_students.through
    extra = 1

    class Meta:
        verbose_name = "Finished student"
        verbose_name_plural = "Finished students"


class AchievementCoach(admin.TabularInline):
    model = Achievement.assigned_coaches.through
    extra = 1

    class Meta:
        verbose_name = "Assigned coach"
        verbose_name_plural = "Assigned coaches"

    def __str__(self):
        return f"Achievement Coach"


@admin.register(Achievement)
class AchievementPage(admin.ModelAdmin):
    change_list_template = 'ach_admin/admin.html'
    form = AchievementForm
    # filter_horizontal = ('subscribed_students', 'assigned_coaches', 'finished_students',)


@admin.register(AchTeacher)
class TeacherPage(admin.ModelAdmin):
    change_list_template = 'ach_admin/admin.html'
    model = AchTeacher
    inlines = [AchievementCoach, ]


@admin.register(AchStudent)
class StudentPage(admin.ModelAdmin):
    change_list_template = 'ach_admin/admin.html'
    model = AchStudent
    inlines = [AchievementSubscribed, AchievementFinished, ]


site.register(Achievement, AchievementPage)
site.register(AchTeacher, TeacherPage)
site.register(AchStudent, StudentPage)
