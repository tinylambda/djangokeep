from django.contrib import admin
from django.db import models
from django.utils.formats import number_format

from django.utils.translation import gettext_lazy as _


class ProjectType(models.Model):
    # use code to establish relationship with other entities
    code = models.IntegerField(_("type code"), unique=True)
    name = models.CharField(_("name"), max_length=128, unique=True)
    standard_price = models.IntegerField(_("standard price"), blank=True, null=True)
    remarks = models.TextField(_("remarks"), blank=True, null=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("project type")
        verbose_name_plural = _("project types")

    def __str__(self):
        standard_price = (
            "null" if self.standard_price is None else self.standard_price_localized()
        )
        return f"{self.name} standard price = {standard_price}"

    @admin.display(description="current standard price")
    def standard_price_localized(self):
        if self.standard_price is None:
            return "-"
        return number_format(self.standard_price, force_grouping=True)
