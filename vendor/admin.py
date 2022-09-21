from django.contrib import admin
from django.db import models
from django.db.models import QuerySet
from django.forms import CheckboxSelectMultiple

from vendor.models import Vendor


@admin.action(description="Mark vendor as vetted")
def mark_vendor_as_vetted(modeladmin, request, queryset: QuerySet):
    queryset.update(vetted=True)


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ("user", "vetted", "date_updated", "date_added")

    filter_horizontal = ("desired_project_type",)
    formfield_overrides = {models.ManyToManyField: {"widget": CheckboxSelectMultiple}}
    autocomplete_fields = ("user",)
    actions = (mark_vendor_as_vetted,)
