from django.db import models
from django.utils.translation import gettext_lazy as _

from account.models import User
from basedata.models import ProjectType


class Vendor(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    desired_project_type = models.ManyToManyField(ProjectType)
    date_updated = models.DateTimeField(auto_now=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("vendor")
        verbose_name_plural = _("vendors")

    def __str__(self):
        return f"Vendor(id={self.user.id}, email={self.user.email})"
