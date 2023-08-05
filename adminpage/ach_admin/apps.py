from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AchAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ach_admin'
    verbose_name = _('Achievement admin')

    def ready(self):
        from . import signals
