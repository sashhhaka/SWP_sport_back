from django.contrib import admin

admin.site.site_url = 'http://127.0.0.1:8000/ach_admin/'

# Register your models here.

# test
from .models import Question
# base
from .models import Achievement, AchTeacher, AchStudent


class achievementPage(admin.ModelAdmin):
    change_list_template = 'ach_admin/admin.html'
    filter_horizontal = ('subscribed_students', 'assigned_coaches', 'finished_students',)


class teacherPage(admin.ModelAdmin):
    filter_horizontal = ('assigned_achievements',)


class studentPage(admin.ModelAdmin):
    filter_horizontal = ('finished_achievements', 'current_achievements',)


# admin.site.register(Question)
admin.site.register(Achievement, achievementPage)
admin.site.register(AchTeacher, teacherPage)
admin.site.register(AchStudent, studentPage)
#admin.site.register(Achievement)
#admin.site.register(AchTeacher)
#admin.site.register(AchStudent)
