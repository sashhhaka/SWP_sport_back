from django.contrib import admin

from sport.models import Group


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_filter = (
        "name",
        "semester",
        "is_club",
        ("sport", admin.RelatedOnlyFieldListFilter),
        ("trainer", admin.RelatedOnlyFieldListFilter),
    )

    list_display = (
        "__str__",
        "sport",
        "is_club",
        "trainer",
    )

    class Media:
        js = (
            "sport/js/list_filter_collapse.js",
        )
