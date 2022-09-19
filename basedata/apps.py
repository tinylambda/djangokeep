from django.apps import AppConfig

from django.utils.translation import gettext_lazy as _


class BasedataConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "basedata"
    verbose_name = _("Base data")
