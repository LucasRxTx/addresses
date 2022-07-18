import numpy as np
import pgeocode
import pycountry
from django.utils.translation import gettext as _
from rest_framework import serializers

from address.models import Address

countries_with_required_post_code = {
    "DZA",
    "ARG",
    "ARM",
    "AUS",
    "AUT",
    "AZE",
    "PRT",
    "BGD",
    "BLR",
    "BEL",
    "BIH",
    "BRA",
    "BRN",
    "BGR",
    "CAN",
    "CHN",
    "COL",
    "HRV",
    "CYP",
    "CZE",
    "DNK",
    "ECU",
    "GBR",
    "EST",
    "FRO",
    "FIN",
    "FRA",
    "GEO",
    "DEU",
    "GRC",
    "GRL",
    "GUM",
    "GGY",
    "NLD",
    "HUN",
    "IND",
    "IDN",
    "ISR",
    "ITA",
    "JPN",
    "JEY",
    "KAZ",
    "KOR",
    "FSM",
    "KGZ",
    "LVA",
    "LIE",
    "LTU",
    "LUX",
    "MKD",
    "MDG",
    "PRT",
    "MYS",
    "MHL",
    "MTQ",
    "MYT",
    "MEX",
    "MNG",
    "MNE",
    "NLD",
    "NZL",
    "GBR",
    "NOR",
    "PAK",
    "PHL",
    "POL",
    "FSM",
    "PRT",
    "PRI",
    "REU",
    "RUS",
    "SAU",
    "SRB",
    "SGP",
    "SVK",
    "SVN",
    "ZAF",
    "ESP",
    "LKA",
    "SXM",
    "VIR",
    "VIR",
    "SWE",
    "CHE",
    "TWN",
    "TJK",
    "THA",
    "TUN",
    "TUR",
    "TKM",
    "VIR",
    "UKR",
    "GBR",
    "USA",
    "URY",
    "UZB",
    "VAT",
    "VNM",
    "GBR",
    "FSM",
}


class AddressSerializers(serializers.ModelSerializer):
    # TODO: Impementation assumes frontend with localize for it's self.
    #   Futre iteration should consider returning localizations for fields,
    #   Or providing an endpoint to get them.
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Address
        fields = (
            "id",
            "user",
            "first_name",
            "last_name",
            "address1",
            "address2",
            "city",
            "postal_code",
            "country",
        )
        read_only_fields = ("id",)

    def validate(self, attrs):
        country = attrs["country"].upper()
        postal_code = attrs.get("postal_code").upper()

        if country in countries_with_required_post_code:
            if not attrs.get("postal_code"):
                raise serializers.ValidationError(
                    {
                        "postal_code": _("Postal code is required."),
                    }
                )

            country_data = pycountry.countries.lookup(country)
            country_validation_error = serializers.ValidationError(
                {
                    "country": _("Country is invalid."),
                }
            )

            if not country_data:
                raise serializers.ValidationError from country_validation_error

            try:
                geo_data = pgeocode.Nominatim(country_data.alpha_2)
            except ValueError:
                raise serializers.ValidationError from country_validation_error

            post_code_data = geo_data.query_postal_code(postal_code)

            if post_code_data["country_code"] is np.nan:
                raise serializers.ValidationError(
                    _("Postal code not found in country.")
                )

        return attrs

    def validate_country(self, value):
        country = None
        print(value)
        if len(value) == 2:
            country = pycountry.countries.get(alpha_2=value)
        elif len(value) == 3:
            country = pycountry.countries.get(alpha_3=value)

        if not country:
            raise serializers.ValidationError(_("Invalid country code."))

        return country.alpha_3
