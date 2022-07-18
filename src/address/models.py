import pycountry
from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _
from django.utils.translation import pgettext, pgettext_lazy


# Create your models here.
class Address(models.Model):
    COUNTRY_CHOICES = tuple(
        (country.alpha_3, pgettext_lazy("Country name", country.name))
        for country in pycountry.countries
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    first_name = models.CharField(_("First name"), max_length=1024)
    last_name = models.CharField(_("Last name"), max_length=1024)
    address1 = models.CharField(_("Address line 1"), max_length=1024)
    address2 = models.CharField(
        _("Address line 2"), default="", blank=True, max_length=1024
    )
    city = models.CharField(_("City"), max_length=1024)
    postal_code = models.CharField(
        # reference http://www.grcdi.nl/pidm/postal%20code.html
        _("Postal code"),
        max_length=10,
        default="",
    )
    country = models.CharField(
        _("Country"),
        choices=COUNTRY_CHOICES,
        max_length=1024,
    )

    class Meta:
        verbose_name_plural = pgettext(
            "Many addresses to a residence.",
            "Addresses",
        )
