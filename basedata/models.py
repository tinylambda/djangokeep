from django.contrib import admin
from django.db import models
from django.utils.formats import number_format

from django.utils.translation import gettext_lazy as _


class ProjectType(models.Model):
    # use code to establish relationship with other entities
    code = models.IntegerField(_("type code"), unique=True)
    name = models.CharField(_("name"), max_length=128, unique=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("project type")
        verbose_name_plural = _("project types")

    def __str__(self) -> str:
        return self.name


class ProfileVendorPrice(models.Model):
    vendor = models.ForeignKey(
        "vendor.Vendor",
        on_delete=models.DO_NOTHING,
    )
    project_type = models.ForeignKey(
        ProjectType,
        on_delete=models.DO_NOTHING,
        to_field="code",
    )
    price_inferred = models.PositiveIntegerField(
        _("inferred price"),
        blank=True,
        null=True,
    )
    ratio_of_customer_price = models.FloatField(
        _("ratio of customer price"),
        default=0.0,
    )

    @admin.display(description="Price inferred currency")
    def price_inferred_currency(self, default="-"):
        if self.price_inferred is not None:
            price_inferred_grouped = number_format(
                self.price_inferred,
                force_grouping=True,
            )
            return f"$ {price_inferred_grouped}"
        return default

    @admin.display(description=_("Ratio of customer price"))
    def ratio_of_customer_price_percent(self):
        return "{:.2%}".format(self.ratio_of_customer_price)
