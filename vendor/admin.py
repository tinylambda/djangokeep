from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple

from vendor.models import Vendor


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ("user", "date_updated", "date_added")

    filter_horizontal = ("desired_project_type",)
    formfield_overrides = {models.ManyToManyField: {"widget": CheckboxSelectMultiple}}
    autocomplete_fields = ("user",)
