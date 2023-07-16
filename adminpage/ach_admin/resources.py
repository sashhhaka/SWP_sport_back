from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, DateWidget
from .models import AchievementAchStudent, Achievement, AchStudent
import datetime
import csv
from import_export.formats.base_formats import CSV


class CustomCSVFormatter(CSV):
    def create_dataset(self, in_stream, **kwargs):
        dataset = super().create_dataset(in_stream, **kwargs)
        for row in dataset.dict:
            # Remove 'date_achieved' key if the value is empty
            if not row.get('Date Achieved'):
                del row['Date Achieved']
        return dataset


class AchievementAchStudentResource(resources.ModelResource):
    achievement_title = fields.Field(
        column_name='Achievement Title',
        attribute='achievement',
        widget=ForeignKeyWidget(Achievement, 'title')
    )
    ach_student_email = fields.Field(
        column_name='Student Email',
        attribute='ach_student',
        widget=ForeignKeyWidget(AchStudent, 'user__email')
    )
    date_achieved = fields.Field(
        column_name='Date Achieved',
        attribute='date_achieved'
    )
    status = fields.Field(
        column_name='Status',
        attribute='status'
    )

    def before_import_row(self, row, **kwargs):
        # Convert achievement title to achievement object
        achievement_title = row.get('Achievement Title')
        if achievement_title:
            achievement = Achievement.objects.filter(title=achievement_title).first()
            row['Achievement Title'] = achievement

        # Convert ach_student email to ach_student object
        ach_student_email = row.get('Student Email')
        if ach_student_email:
            ach_student = AchStudent.objects.filter(user__email=ach_student_email).first()
            row['Ach Student Email'] = ach_student

        # Update the 'status' attribute with the value from the 'Status' column
        status = row.get('Status')
        if status:
            row['status'] = status

        date_achieved = row.get('Date Achieved')
        if date_achieved:
            row['date_achieved'] = date_achieved
        else:
            row['date_achieved'] = datetime.date.today()

    class Meta:
        model = AchievementAchStudent
        fields = ('achievement_title', 'ach_student_email', 'date_achieved', 'status')
        import_id_fields = ('achievement_title', 'ach_student_email', 'date_achieved')
        export_order = ('achievement_title', 'ach_student_email', 'date_achieved', 'status')
        skip_unchanged = True
        report_skipped = False
