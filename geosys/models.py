from django.db import models
from django.utils.translation import gettext_lazy as _


class AddressType(models.Model):
    """Model for storing address types"""

    name = models.CharField(_("Nom"), max_length=255)

    class Meta:
        verbose_name = _("Type d'addresse")
        verbose_name_plural = _("Types d'addresse")

    def __str__(self):
        return self.name


class Address(models.Model):
    """Model for storing addresses"""

    name = models.CharField(_("Nom"), max_length=255)
    label = models.CharField(_("Libellé"), max_length=255)

    country = models.ForeignKey("geosys.Country", on_delete=models.CASCADE)
    department = models.ForeignKey("geosys.Department", on_delete=models.CASCADE)
    region = models.ForeignKey("geosys.Region", on_delete=models.CASCADE)
    city = models.ForeignKey("geosys.City", on_delete=models.CASCADE)
    street = models.ForeignKey("geosys.Street", on_delete=models.CASCADE)

    address_type = models.ForeignKey("geosys.AddressType", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Addresse")
        verbose_name_plural = _("Addresses")

    def __str__(self):
        return self.name


class Continent(models.Model):
    """Model for storing continents"""

    code = models.CharField(_("Code"), max_length=255, primary_key=True)
    name = models.CharField(_("Nom"), max_length=255)
    slug = models.SlugField(_("Slug"), max_length=255)

    class Meta:
        verbose_name = _("Continent")
        verbose_name_plural = _("Continents")

    def __str__(self):
        return self.name


class Country(models.Model):
    """Model for storing countries"""

    iso_name = models.CharField(_("Nom ISO"), max_length=255)
    name = models.CharField(_("Nom"), max_length=255, unique=True)
    short_name = models.CharField(_("Nom court"), max_length=255, null=True)
    numeric_code = models.CharField(_("Code numérique"), max_length=255, unique=True)
    alpha_3_code = models.CharField(_("Code alpha-3"), max_length=255, unique=True)
    alpha_2_code = models.CharField(_("Code alpha-2"), max_length=255, unique=True, primary_key=True)
    subdivision_code = models.CharField(_("Code de subdivision"), max_length=255, unique=True)
    tld = models.CharField(_("TLD"), max_length=255, unique=True)  # Top Level Domain
    is_independent = models.BooleanField(_("Est indépendant"), default=True)

    continent = models.ForeignKey("geosys.Continent", on_delete=models.CASCADE, related_name="country_continent")
    # TODO: maybe add sovereign state ( create a model for mondial organizations like UN, EU, etc. It can be a country too) for now owner_countries does the job
    owner_countries = models.ManyToManyField("geosys.Country", related_name="country_owner_countries")
    country_data = models.OneToOneField("geosys.CountryData", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Pays")
        verbose_name_plural = _("Pays")
        ordering = ["iso_name"]

    def __str__(self):
        return self.name


class CountryData(models.Model):
    """Model for storing country data"""

    phone_code = models.CharField(_("Code téléphonique"), max_length=255)
    population = models.IntegerField(_("Population"))
    area = models.FloatField(_("Superficie"))
    density = models.FloatField(_("Densité"))
    gpd = models.FloatField(_("PIB"))
    gpd_per_capita = models.FloatField(_("PIB par habitant"))
    currency = models.ForeignKey("geosys.Currency", on_delete=models.CASCADE)
    main_language = models.ForeignKey("geosys.Language", on_delete=models.CASCADE)
    languages = models.ManyToManyField("geosys.Language", related_name="country_languages")


class CountryLevel(models.Model):
    """Model for storing country levels"""

    name = models.CharField(_("Nom"), max_length=255)
    abreviation = models.CharField(_("Abréviation"), max_length=255)
    alpha_3_code = models.CharField(_("Code ISO 3166-1"), max_length=255)
    alpha_2_code = models.CharField(_("Code ISO 3166-1"), max_length=255)
    iso_3166_2_code = models.CharField(_("Code ISO 3166-2"), max_length=255)  # FR-CVL for Centre-Val de Loire
    local_code = models.CharField(_("Code INSEE"), max_length=255)  # Code INSEE for France
    slug = models.SlugField(_("Slug"), max_length=255)

    class Meta:
        abstract = True
        verbose_name = _("Niveau de pays")
        verbose_name_plural = _("Niveaux de pays")

    def __str__(self):
        return self.name


class Region(CountryLevel, models.Model):
    """Model for storing regions"""

    country = models.ForeignKey("geosys.Country", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Région")
        verbose_name_plural = _("Régions")

    def __str__(self):
        return self.name


class Department(CountryLevel, models.Model):
    """Model for storing departments"""

    region = models.ForeignKey("geosys.Region", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Département")
        verbose_name_plural = _("Départements")

    def __str__(self):
        return self.name


class CityType(models.Model):
    """Model for storing city types"""

    name = models.CharField(_("Nom"), max_length=255)

    class Meta:
        verbose_name = _("Type de ville")
        verbose_name_plural = _("Types de ville")

    def __str__(self):
        return self.name


class City(models.Model):
    """Model for storing cities"""

    name = models.CharField(_("Nom"), max_length=255)
    zip_code = models.CharField(_("Code postal"), max_length=255)  # Code commune in france
    postal_code = models.CharField(_("Code postal"), max_length=255)
    city_type = models.ForeignKey("geosys.CityType", on_delete=models.CASCADE)
    slug = models.SlugField(_("Slug"), max_length=255)

    region = models.ForeignKey("geosys.Region", on_delete=models.CASCADE, null=True)
    department = models.ForeignKey("geosys.Department", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = _("Ville")
        verbose_name_plural = _("Villes")

    def __str__(self):
        return self.name


class Street(models.Model):
    """Model for storing streets"""

    number = models.CharField(_("Numéro"), max_length=255)
    label = models.ForeignKey("geosys.StreetLabel", on_delete=models.CASCADE)  # Street, Avenue, Boulevard, etc.
    name = models.CharField(_("Nom"), max_length=255)
    alt_name = models.CharField(_("Nom alternatif"), max_length=255)

    alt_slug = models.SlugField(_("Slug alternatif"), max_length=255)

    city = models.ForeignKey("geosys.City", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Rue")
        verbose_name_plural = _("Rues")
        ordering = ["label", "name"]

    def __str__(self):
        return self.name


class StreetLabel(models.Model):
    """Model for storing street labels"""

    name = models.CharField(_("Nom"), max_length=255)

    class Meta:
        verbose_name = _("Libellé de rue")
        verbose_name_plural = _("Libellés de rue")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Language(models.Model):
    """Model for storing languages"""

    name = models.CharField(_("Nom"), max_length=255)
    slug = models.SlugField(_("Slug"), max_length=255)

    class Meta:
        verbose_name = _("Langue")
        verbose_name_plural = _("Langues")

    def __str__(self):
        return self.name


class Currency(models.Model):
    """Model for storing currencies"""

    name = models.CharField(_("Nom"), max_length=255)
    iso_code = models.CharField(_("Code ISO"), max_length=255, primary_key=True)
    iso_number = models.CharField(_("Code numérique ISO"), max_length=255)
    decimals = models.IntegerField(_("Décimales"), default=2)
    symbol = models.CharField(_("Symbole"), max_length=255)
    rank = models.IntegerField(_("Rang"), default=0)

    class Meta:
        verbose_name = _("Devise")
        verbose_name_plural = _("Devises")

    def __str__(self):
        return self.name


class PhoneNumberType(models.Model):
    """Model for storing phone number types"""

    name = models.CharField(_("Nom"), max_length=255)

    class Meta:
        verbose_name = _("Type de numéro de téléphone")
        verbose_name_plural = _("Types de numéro de téléphone")

    def __str__(self):
        return self.name


class PhoneNumber(models.Model):
    """Model for storing phone numbers"""

    country_code = models.CharField(_("Code pays"), max_length=255)
    number = models.CharField(_("Numéro"), max_length=255)
    label = models.CharField(_("Libellé"), max_length=255)

    type = models.ForeignKey("geosys.PhoneNumberType", on_delete=models.CASCADE)
    country = models.ForeignKey("geosys.Country", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Numéro de téléphone")
        verbose_name_plural = _("Numéros de téléphone")

    def __str__(self):
        return self.number


class Email(models.Model):
    """Model for storing emails"""

    label = models.CharField(_("Libellé"), max_length=255)
    email = models.EmailField(_("Email"), unique=True)

    class Meta:
        verbose_name = _("Email")
        verbose_name_plural = _("Emails")

    def __str__(self):
        return self.email
