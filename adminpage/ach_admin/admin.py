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



"""Inlines for ach_student and ach_teacher
Enable many-to-many relationship in admin page for them
"""


class AchievementSubscribedStudent(admin.TabularInline):
    model = Achievement.students.through
    extra = 1
    show_change_link = False

    class Meta:
        verbose_name = "Subscribed student"
        verbose_name_plural = "Subscribed students"

    def __str__(self):
        return f"Achievement Subscribed"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(status='subscribed')


class AchievementFinishedStudent(admin.TabularInline):
    model = Achievement.students.through
    extra = 1

    class Meta:
        verbose_name = "Finished student"
        verbose_name_plural = "Finished students"

    def __str__(self):
        return f"Achievement Finished"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(status='finished')

    def clean(self, form, formset):
        super().clean(form, formset)
        if form.cleaned_data.get('status') == 'finished' and not form.cleaned_data.get('date_achieved'):
            form.add_error('date_achieved', 'This field is required for finished achievements.')



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
    # filter_horizontal = ('assigned_coaches')
    inlines = [AchievementSubscribedStudent, AchievementFinishedStudent]
    list_display = ['title', 'get_subscribed_students', 'get_finished_students']
    search_fields = ['title']

    # cahnge inlines names
    def get_inline_instances(self, request, obj=None):
        inline_instances = []
        for inline_class in self.inlines:
            if inline_class == AchievementSubscribedStudent:
                inline = inline_class(self.model, self.admin_site)
                inline.verbose_name_plural = 'Subscribed students'
                inline_instances.append(inline)
            elif inline_class == AchievementFinishedStudent:
                inline = inline_class(self.model, self.admin_site)
                inline.verbose_name_plural = 'Finished students'
                inline_instances.append(inline)
            else:
                inline = inline_class(self.model, self.admin_site)
                inline_instances.append(inline)
        return inline_instances

    def get_subscribed_students(self, obj):
        return obj.subscribed_students().count() if obj.subscribed_students() else 'No subscribed students'

    get_subscribed_students.short_description = 'Subscribed Students Count'

    def get_finished_students(self, obj):
        return obj.finished_students().count() if obj.finished_students() else 'No finished students'

    get_finished_students.short_description = 'Finished Students Count'



@admin.register(AchTeacher)
class TeacherPage(admin.ModelAdmin):
    change_list_template = 'ach_admin/admin.html'
    model = AchTeacher
    inlines = [AchievementCoach, ]
    search_fields = ['user__email', 'user__first_name', 'user__last_name']

    # def get_num_assigned_achievements(self, obj):
    #     return obj.assigned_achievements.count()
    #
    # get_num_assigned_achievements.short_description = 'Assigned Achievements'
    #
    # list_display = ['user', 'get_num_assigned_achievements']


@admin.register(AchStudent)
class StudentPage(admin.ModelAdmin):
    change_list_template = 'ach_admin/admin.html'
    model = AchStudent
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    inlines = [
        # AchievementSubscribed, AchievementFinished,
        AchievementSubscribedStudent, AchievementFinishedStudent,
    ]

    def get_inline_instances(self, request, obj=None):
        inline_instances = super().get_inline_instances(request, obj)
        subscribed_inline = next((inline for inline in inline_instances if isinstance(inline, AchievementSubscribedStudent)),
                                 None)
        finished_inline = next((inline for inline in inline_instances if isinstance(inline, AchievementFinishedStudent)), None)
        if subscribed_inline and finished_inline:
            subscribed_inline.show_change_link = False
            finished_inline.show_change_link = False
            subscribed_inline.verbose_name_plural = "Current Student Achievements"
            finished_inline.verbose_name_plural = "Finished Student Achievements"
        return inline_instances

    # def get_num_subscribed_achievements(self, obj):
    #     return obj.achievementachstudent_set.filter(status='subscribed').count()
    #
    # def get_num_finished_achievements(self, obj):
    #     return obj.achievementachstudent_set.filter(status='finished').count()
    #
    # get_num_subscribed_achievements.short_description = 'Subscribed Achievements'
    # get_num_finished_achievements.short_description = 'Finished Achievements'
    #
    # list_display = ['user', 'get_num_subscribed_achievements', 'get_num_finished_achievements']


site.register(Achievement, AchievementPage)
site.register(AchTeacher, TeacherPage)
site.register(AchStudent, StudentPage)
