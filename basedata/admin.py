from django.contrib import admin

from .models import ProjectType, ProfileVendorPrice


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
        "date_updated",
        "date_added",
    )

    fields = (
        "code",
        "name",
    )


@admin.register(ProfileVendorPrice)
class ProfileVendorProfileAdmin(BaseDataModelAdmin):
    list_display = (
        "vendor",
        "project_type",
        "price_inferred",
        "ratio_of_customer_price_percent",
    )

    fields = ("vendor", "project_type", "price_inferred", "ratio_of_customer_price")

    readonly_fields = ("ratio_of_customer_price_percent",)
