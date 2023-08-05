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
        attribute='date_achieved',
    )
    status = fields.Field(
        column_name='Status',
        attribute='status'
    )

    def before_import_row(self, row, **kwargs):
        achievement_title = row.get('Achievement Title')
        ach_student_email = row.get('Student Email')
        status = row.get('Status')
        date_achieved = row.get('Date Achieved')

        # Check if the record already exists in the database
        existing_instance = AchievementAchStudent.objects.filter(
            achievement__title=achievement_title,
            ach_student__user__email=ach_student_email
        ).first()

        if existing_instance:
            # Delete the existing instance
            existing_instance.delete()
            # update tag

        # Continue with importing the row
        return row

    def before_save_instance(self, instance, using_transactions, dry_run):
        # Check if the record already exists in the database
        existing_instance = AchievementAchStudent.objects.filter(
            achievement=instance.achievement,
            ach_student=instance.ach_student
        ).first()

        if existing_instance:
            # Delete the existing instance
            existing_instance.delete()

        return instance

    class Meta:
        model = AchievementAchStudent
        fields = ('achievement_title', 'ach_student_email', 'date_achieved', 'status')
        import_id_fields = ('achievement_title', 'ach_student_email', 'date_achieved')
        export_order = ('achievement_title', 'ach_student_email', 'date_achieved', 'status')
        skip_unchanged = True
        report_skipped = True

