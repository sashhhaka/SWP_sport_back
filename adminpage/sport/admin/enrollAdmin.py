from django.contrib import admin

from .fabrics import semester_filter_fabric
from .mixins import EnrollExportCsvMixin


class EnrollAdmin(admin.ModelAdmin, EnrollExportCsvMixin):
    list_filter = [semester_filter_fabric("group__semester__id")]
    actions = ["export_as_csv"]
