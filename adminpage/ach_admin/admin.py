
from sport.admin.site import site
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.forms.models import BaseInlineFormSet
from datetime import date

admin.site.site_url = 'http://127.0.0.1:8000/ach_admin/'

from .models import Achievement, AchTeacher, AchStudent, AchievementAchStudent
from .forms import AchievementForm



from django import forms
from .models import AchievementAchStudent


'''Logic for achievement statuses'''
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




class SubscribedStudentFormSet(BaseInlineFormSet):
    """
    Formset for subscribed students in the AchievementSubscribedStudent inline.
    Sets the default status as 'subscribed' and initializes date_achieved as None.
    """

    def get_default_status(self):
        return 'subscribed'

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs.setdefault('initial', {})
        kwargs['initial']['status'] = self.get_default_status()
        kwargs['initial']['date_achieved'] = None
        return kwargs


class AchievementSubscribedStudent(admin.TabularInline):
    """
    Inline for subscribed students in the Achievement admin page.
    Uses the SubscribedStudentFormSet as the formset.
    """

    model = Achievement.students.through
    extra = 1
    show_change_link = False
    formset = SubscribedStudentFormSet

    class Meta:
        verbose_name = "Subscribed student"
        verbose_name_plural = "Subscribed students"

    def __str__(self):
        return f"Achievement Subscribed"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(status='subscribed')

    # fill the date_achieved with today date if status is changed to finished


class FinishedStudentFormSet(BaseInlineFormSet):
    """
    Formset for finished students in the AchievementFinishedStudent inline.
    Sets the default status as 'finished' and initializes date_achieved based on the instance's value or today's date.
    """

    def get_default_status(self):
        return 'finished'

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs.setdefault('initial', {})
        kwargs['initial']['status'] = self.get_default_status()

        if kwargs['initial']['status'] == 'finished':
            if 'instance' in kwargs:
                kwargs['initial']['date_achieved'] = kwargs['instance'].date_achieved
            else:
                kwargs['initial']['date_achieved'] = date.today()

        return kwargs


class AchievementFinishedStudent(admin.TabularInline):
    """
    Inline for finished students in the Achievement admin page.
    Uses the FinishedStudentFormSet as the formset.
    """

    model = Achievement.students.through
    extra = 1
    show_change_link = False
    formset = FinishedStudentFormSet

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
        if form.cleaned_data.get('status') == 'finished':
            # Remove the requirement for date_achieved
            form.cleaned_data['date_achieved'] = None



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

    def save_formset(self, request, form, formset, change):
        if formset.model == Achievement.students.through:
            instances = formset.save(commit=False)
            for instance in instances:
                if instance.status == 'finished' and not instance.date_achieved:
                    instance.date_achieved = date.today()
                instance.save()
        else:
            super().save_formset(request, form, formset, change)

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
        subscribed_inline = next(
            (inline for inline in inline_instances if isinstance(inline, AchievementSubscribedStudent)),
            None)
        finished_inline = next(
            (inline for inline in inline_instances if isinstance(inline, AchievementFinishedStudent)), None)
        if subscribed_inline and finished_inline:
            subscribed_inline.show_change_link = False
            finished_inline.show_change_link = False
            subscribed_inline.verbose_name_plural = "Current Student Achievements"
            finished_inline.verbose_name_plural = "Finished Student Achievements"
        return inline_instances


site.register(Achievement, AchievementPage)
site.register(AchTeacher, TeacherPage)
site.register(AchStudent, StudentPage)
