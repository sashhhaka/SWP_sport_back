import csv

from django.http import HttpResponse

from sport.models import Semester


class EnrollExportCsvMixin:
    def export_as_csv(self, request, queryset):
        field_names = ["Sport", "Fullname", "Email"]
        response = HttpResponse(content_type='text/csv')
        semester_id = request.GET.get("semester")
        if semester_id is None:
            semester_name = "all"
        else:
            semester_name = Semester.objects.get(pk=semester_id).name
        response['Content-Disposition'] = f'attachment; filename=SportEnrollment_{semester_name}.csv'
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            group = obj.group
            sport = group.sport
            sport_name = "Personal Trainer" if sport.special and not group.is_club else sport.name

            student_fullname = str(obj.student)
            student_email = obj.student.email

            writer.writerow([sport_name, student_fullname, student_email])

        return response

    export_as_csv.short_description = "Export Selected"
