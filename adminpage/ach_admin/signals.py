from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission


from django.db.models.signals import m2m_changed, post_save, pre_save
from django.dispatch.dispatcher import receiver

from ach_admin.models import AchStudent, AchTeacher


User = get_user_model()


def get_current_group_mapping():
    group_mapping = {}
    user_groups = Group.objects.filter(
        verbose_name__in=[
            settings.STUDENT_AUTH_GROUP_VERBOSE_NAME,
            settings.TRAINER_AUTH_GROUP_VERBOSE_NAME,
        ],
    ).all()

    for group in user_groups:
        group_mapping.update({group.verbose_name: group.pk})

    return group_mapping


@receiver(
    m2m_changed,
    sender=User.groups.through
)
# if user is add to a group, this will create a corresponding profile
@receiver(m2m_changed, sender=User.groups.through)
def create_student_profile(instance, action, reverse, pk_set, **kwargs):
    if not reverse:
        group_mapping = get_current_group_mapping()

        if group_mapping.get(
            settings.STUDENT_AUTH_GROUP_VERBOSE_NAME,
            None
        ) in pk_set:
            if action == "post_add":

                ach_student, ach_created = AchStudent.objects.get_or_create(user=instance)
                if ach_created:
                    ach_student.save()

            elif action == "pre_remove":
                AchStudent.objects.filter(user=instance).delete()

        if group_mapping.get(settings.TRAINER_AUTH_GROUP_VERBOSE_NAME, None) in pk_set:
            if action == "post_add":
                # AchTeacher.objects.get_or_create(pk=instance.pk)
                ach_teacher, ach_created = AchTeacher.objects.get_or_create(user=instance)
                if ach_created:
                    ach_teacher.save()
