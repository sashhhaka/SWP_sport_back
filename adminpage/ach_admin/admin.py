from django.contrib import admin
from sport.admin.site import site
from django.urls import reverse
from django.shortcuts import redirect

admin.site.site_url = 'http://127.0.0.1:8000/ach_admin/'

from .models import Achievement, AchTeacher, AchStudent, AchievementAchStudent
from .forms import AchievementForm


'''Logic for achievement statuses'''

from django import forms
from .models import AchievementAchStudent


class AchievementAchStudentForm(forms.ModelForm):
    class Meta:
        model = AchievementAchStudent
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.status != 'finished':
            self.fields['date_achieved'].required = False


class AchievementAchStudentAdmin(admin.ModelAdmin):
    form = AchievementAchStudentForm
    list_display = ('ach_student', 'achievement', 'status', 'is_achieved', 'date_achieved')
    list_filter = ('status', 'achievement')
    search_fields = ('ach_student__user__email', 'achievement__title')


site.register(AchievementAchStudent, AchievementAchStudentAdmin)


"""Logic for achievement statuses achstudents"""

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import AchStudent, AchievementAchStudent


class AchievementAchStudentInline(admin.TabularInline):
    model = AchievementAchStudent
    extra = 0
    readonly_fields = ['achievement', 'status', 'assign_button']
    fields = ['achievement', 'status', 'assign_button']
    ordering = ['achievement__title']

    def has_add_permission(self, request, obj):
        return False

    def assign_button(self, instance):
        if instance.status != 'finished':
            url = reverse('admin:ach_admin_achievementachstudent_change', args=(instance.id,))
            return format_html('<a class="button" href="{}">Assign</a>', url)
        return ''

    assign_button.short_description = 'Assign'


class AchStudentAdmin(admin.ModelAdmin):
    inlines = [AchievementAchStudentInline]
    list_display = ['user', 'assigned_achievements']
    search_fields = ['user__email']

    def assigned_achievements(self, obj):
        return obj.achievementachstudent_set.count()

    assigned_achievements.short_description = 'Assigned Achievements'


site.register(AchStudent, AchStudentAdmin)








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


#@admin.register(AchStudent)
#class StudentPage(admin.ModelAdmin):
#    change_list_template = 'ach_admin/admin.html'
#    model = AchStudent
#    inlines = [AchievementSubscribed, AchievementFinished, ]


site.register(Achievement, AchievementPage)
site.register(AchTeacher, TeacherPage)
#site.register(AchStudent, StudentPage)
