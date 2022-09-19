from django import forms
from django.contrib import admin

from .models import ProjectType


class BaseDataModelAdmin(admin.ModelAdmin):
    """base data should stay stable"""

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return True


@admin.register(ProjectType)
class ProjectTypeAdmin(BaseDataModelAdmin):
    list_display = (
        "code",
        "name",
        "standard_price_localized",
        "remarks",
        "date_updated",
        "date_added",
    )

    fields = (
        "code",
        "name",
        "standard_price",
        "standard_price_localized",
        "remarks",
    )
    readonly_fields = ("standard_price_localized",)
