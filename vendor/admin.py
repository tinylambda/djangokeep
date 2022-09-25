from django.contrib import admin
from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.db.models import QuerySet
from django.forms import CheckboxSelectMultiple, BaseInlineFormSet

from basedata.models import ProjectType, ProfileVendorPrice
from vendor.models import Vendor, VendorPrice


@admin.action(description="Mark vendor as vetted")
def mark_vendor_as_vetted(modeladmin, request, queryset: QuerySet):
    queryset.update(vetted=True)


class VendorPriceFormSet(BaseInlineFormSet):
    def __init__(
        self,
        data=None,
        files=None,
        instance=None,
        save_as_new=False,
        prefix=None,
        queryset=None,
        **kwargs,
    ):
        super(VendorPriceFormSet, self).__init__(
            data=data,
            files=files,
            instance=instance,
            save_as_new=save_as_new,
            prefix=prefix,
            queryset=queryset,
            **kwargs,
        )
        self.initial_extra = self.get_initial_extra_data()

    def get_initial_extra_data(self):
        initial_extra = []
        if isinstance(self.instance, Vendor):
            vendor_prices = VendorPrice.objects.filter(vendor=self.instance)
            remain_project_types = ProjectType.objects.exclude(
                code__in=vendor_prices.values("project_type_id")
            )
            for remain_project_type in remain_project_types:
                try:
                    profile_vendor_price = ProfileVendorPrice.objects.get(
                        vendor=self.instance,
                        project_type=remain_project_type,
                    )
                    price_inferred = profile_vendor_price.price_inferred_currency
                    ratio_of_customer_price = (
                        profile_vendor_price.ratio_of_customer_price_percent()
                    )
                except ProfileVendorPrice.DoesNotExist:
                    profile_vendor_price = None
                    price_inferred = ratio_of_customer_price = "-"

                extra_data = {
                    "project_type": remain_project_type.code,
                    "price_inferred": price_inferred,
                    "ratio_of_customer_price": ratio_of_customer_price,
                }
                initial_extra.append(extra_data)
        return initial_extra


class VendorPriceInline(admin.TabularInline):
    def __init__(self, *args, **kwargs):
        super(VendorPriceInline, self).__init__(*args, **kwargs)
        self.project_type_count = self.get_project_type_count()

    model = VendorPrice
    formset = VendorPriceFormSet
    fields = (
        "project_type",
        "price_standard",
        "price_standard_current",
        "price_inferred",
        "ratio_of_customer_price_percent",
    )
    readonly_fields = (
        "project_type",
        "price_standard_current",
        "price_inferred",
        "ratio_of_customer_price_percent",
    )
    show_full_result_count = True
    show_change_link = True

    @classmethod
    def get_project_type_count(cls):
        return ProjectType.objects.count()

    def get_extra(self, request, obj=None, **kwargs):
        qs = self.get_queryset(request)
        extra = self.project_type_count - qs.filter(vendor=obj).count()
        return extra

    def get_max_num(self, request, obj=None, **kwargs):
        return self.project_type_count

    def get_min_num(self, request, obj=None, **kwargs):
        return self.project_type_count


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ("user", "vetted", "date_updated", "date_added")

    formfield_overrides = {models.ManyToManyField: {"widget": CheckboxSelectMultiple}}
    autocomplete_fields = ("user",)
    actions = (mark_vendor_as_vetted,)
    inlines = (VendorPriceInline,)

    def _create_formsets(self, request, obj, change):
        if not change:
            return [], []
        formsets, inline_instances = super(VendorAdmin, self)._create_formsets(
            request, obj, change
        )
        for fs in formsets:
            for f in fs.forms:
                if isinstance(f.instance, VendorPrice):
                    if not hasattr(f.instance, "project_type"):
                        project_type_id = f.initial["project_type"]
                        price_inferred = f.initial["price_inferred"]
                        project_type = ProjectType.objects.get(code=project_type_id)
                        setattr(f.instance, "project_type", project_type)
                        setattr(f.instance, "price_inferred", price_inferred)
        return formsets, inline_instances
