from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import AchTeacher, Achievement, AchStudent

class AchievementForm(forms.ModelForm):
    assigned_coaches = forms.ModelMultipleChoiceField(
        queryset=AchTeacher.objects.all(),
        widget=FilteredSelectMultiple(verbose_name='Assigned Coaches', is_stacked=False),
        required=False,
    )
    subscribed_students = forms.ModelMultipleChoiceField(
        queryset=AchStudent.objects.all(),
        widget=FilteredSelectMultiple(verbose_name='Subscribed Students', is_stacked=False),
        required=False,
    )
    finished_students = forms.ModelMultipleChoiceField(
        queryset=AchStudent.objects.all(),
        widget=FilteredSelectMultiple(verbose_name='Finished Students', is_stacked=False),
        required=False,
    )

    class Media:
        css = {
            'all': ('admin/css/widgets.css',),
        }
        js = ('admin/js/jquery.init.js', 'admin/js/SelectBox.js', 'admin/js/SelectFilter2.js')

    class Meta:
        model = Achievement
        fields = '__all__'
