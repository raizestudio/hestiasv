from django.db import models
from django.utils.translation import gettext_lazy as _


class Menu(models.Model):
    """Model for storing menus"""

    name = models.CharField(_("Nom"), max_length=255)
    description = models.TextField(_("Description"))
    icon = models.CharField(_("Icon"), max_length=255)
    url = models.CharField(_("Lien"), max_length=255)
    order = models.IntegerField(_("Ordre"), default=0)

    groups = models.ManyToManyField("user.Group", related_name="menu_groups", blank=True)

    class Meta:
        verbose_name = "Menu"
        verbose_name_plural = "Menus"

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """Model for storing menu items"""

    name = models.CharField(_("Nom"), max_length=255)
    description = models.TextField(_("Description"))
    icon = models.CharField(_("Icon"), max_length=255)
    url = models.CharField(_("Lien"), max_length=255)
    order = models.IntegerField(_("Ordre"), default=0)

    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

    roles = models.ManyToManyField("user.Role", related_name="menu_items_roles", blank=True)

    class Meta:
        verbose_name = _("Élément de menu")
        verbose_name_plural = _("Éléments de menu")

    def __str__(self):
        return self.name


class Setting(models.Model):
    """Model for storing settings"""

    key = models.CharField(_("Clé"), max_length=255, primary_key=True)
    value = models.TextField(_("Valeur"))

    class Meta:
        abstract = True
        verbose_name = _("Paramètre")
        verbose_name_plural = _("Paramètres")

    def __str__(self):
        return self.key


class AppSetting(Setting):
    """Model for storing app settings"""

    class Meta:
        verbose_name = _("Paramètre de l'application")
        verbose_name_plural = _("Paramètres de l'application")
