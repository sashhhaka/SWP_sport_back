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

    # def before_import_row(self, row, **kwargs):
    #     # Convert achievement title to achievement object
    #     achievement_title = row.get('Achievement Title')
    #     if achievement_title:
    #         achievement = Achievement.objects.filter(title=achievement_title).first()
    #         row['Achievement Title'] = achievement
    #
    #     # Convert ach_student email to ach_student object
    #     ach_student_email = row.get('Student Email')
    #     if ach_student_email:
    #         ach_student = AchStudent.objects.filter(user__email=ach_student_email).first()
    #         row['Student Email'] = ach_student
    #
    #     # Update the 'status' attribute with the value from the 'Status' column
    #     status = row.get('Status')
    #     if status:
    #         row['Status'] = status
    #
    #     # Update the 'date_achieved' attribute with the value from the 'Date Achieved' column
    #     date_achieved = row.get('Date Achieved')
    #     if date_achieved:
    #         row['Date Achieved'] = date_achieved
    #
    #     # Check if the relation already exists in the database
    #     achievement = row.get('Achievement Title')
    #     ach_student = row.get('Student Email')
    #     if achievement and ach_student:
    #         existing_instance = AchievementAchStudent.objects.filter(
    #             achievement=achievement,
    #             ach_student=ach_student
    #         ).first()
    #         if existing_instance:
    #             # Update the existing instance with the new values
    #             for key, value in row.items():
    #                 setattr(existing_instance, key, value)
    #             # Save the updated instance
    #             existing_instance.save()
    #             # Skip importing the row by returning None
    #             return None


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
