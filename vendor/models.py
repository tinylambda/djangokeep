from django.contrib import admin
from django.db import models
from django.utils.formats import number_format
from django.utils.translation import gettext_lazy as _

from account.models import User
from basedata.models import ProjectType, ProfileVendorPrice


class Vendor(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    vetted = models.BooleanField(_("vetted"), default=False)
    date_updated = models.DateTimeField(auto_now=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("vendor")
        verbose_name_plural = _("vendors")

    def __str__(self):
        return self.user.email


class VendorPrice(models.Model):
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.DO_NOTHING,
        related_name="vendor_prices",
    )
    project_type = models.ForeignKey(
        ProjectType,
        on_delete=models.DO_NOTHING,
        related_name="project_type_prices",
        to_field="code",
    )
    price_standard = models.PositiveIntegerField(
        _("standard price"),
        blank=True,
        null=True,
    )
    date_updated = models.DateTimeField(auto_now=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("vendor", "project_type")

    def __str__(self):
        return f"{self.vendor.user.email} with {self.project_type.name}"

    def related_profile_vendor_price(self):
        try:
            profile_vendor_price = ProfileVendorPrice.objects.get(
                vendor=self.vendor,
                project_type=self.project_type,
            )
        except ProfileVendorPrice.DoesNotExist:
            profile_vendor_price = None
        return profile_vendor_price

    @admin.display(description="Current standard price")
    def price_standard_current(self, default="-"):
        if self.price_standard is None:
            return default
        price_standard_grouped = number_format(self.price_standard, force_grouping=True)
        return f"$ {price_standard_grouped}"

    @admin.display(description="Price inferred")
    def price_inferred(self, default="-"):
        profile_vendor_price = self.related_profile_vendor_price()
        if profile_vendor_price is not None and profile_vendor_price.price_inferred:
            return profile_vendor_price.price_inferred_currency()
        return default

    @admin.display(description="Ratio of customer price")
    def ratio_of_customer_price_percent(self, default="-"):
        profile_vendor_price = self.related_profile_vendor_price()
        if (
            profile_vendor_price is not None
            and profile_vendor_price.ratio_of_customer_price
        ):
            return profile_vendor_price.ratio_of_customer_price_percent()
        return default
