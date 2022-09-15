from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models import User


class Process(models.Model):
    """Process instances"""

    owner = models.ForeignKey(User, verbose_name=_("owner"), on_delete=models.CASCADE)
    date_updated = models.DateTimeField(_("date updated"), auto_now=True)
    date_created = models.DateTimeField(_("date created"), auto_now_add=True)

    class Meta:
        verbose_name = _("process")
        verbose_name_plural = _("processes")
