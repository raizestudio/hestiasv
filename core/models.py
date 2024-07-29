from django.contrib.contenttypes.fields import GenericRelation
from django.core.cache import cache
from django.db import models, transaction
from django.db.models import ProtectedError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.exceptions import SoftDeleteException


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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete('app_settings')

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        cache.delete('app_settings')


class Category(models.Model):
    """Model for storing categories"""

    name = models.CharField(_("Nom"), max_length=255)
    color = models.CharField(_("Couleur"), max_length=255)

    class Meta:
        verbose_name = _("Catégorie")
        verbose_name_plural = _("Catégories")

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Model for storing tags"""

    name = models.CharField(_("Nom"), max_length=255)
    color = models.CharField(_("Couleur"), max_length=255)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return self.name


class SoftDeleteQuerySet(models.query.QuerySet):
    def delete(self) -> None:
        """Supprime tous les objects de la classe"""
        for obj in self.all():
            obj.delete()

    def hard_delete(self) -> None:
        """Supprime définitivement l'objet"""
        return super().delete()


class SoftDeleteManager(models.Manager):
    def get_queryset(self) -> SoftDeleteQuerySet:
        """Queryset du modèle"""
        return SoftDeleteQuerySet(self.model, using=self._db).filter(deleted_at__isnull=True)

    def deleted_objects(self) -> SoftDeleteQuerySet:
        """Queryset des objets supprimés"""
        return SoftDeleteQuerySet(self.model, using=self._db).filter(deleted_at__isnull=False)

    def all_objects(self) -> SoftDeleteQuerySet:
        """Queryset de tous les objets"""
        return SoftDeleteQuerySet(self.model, using=self._db)


class SoftDelete(models.Model):
    """Soft delete modèle"""

    deleted_at = models.DateTimeField(blank=True, null=True)
    restored_at = models.DateTimeField(blank=True, null=True)
    deleted_by = models.ForeignKey(
        "user.User",
        on_delete=models.SET_NULL,
        related_name="%(class)s_deleted_by",
        blank=True,
        null=True,
    )
    restored_by = models.ForeignKey(
        "user.User",
        on_delete=models.SET_NULL,
        related_name="%(class)s_restored_by",
        blank=True,
        null=True,
    )

    objects = SoftDeleteManager()

    class Meta:
        abstract = True

    @property
    def is_deleted(self) -> bool:
        """Vérifie si l'objet est supprimé"""
        return self.deleted_at is not None

    @property
    def is_restored(self) -> bool:
        """Vérifie si l'objet est restauré"""
        return self.restored_at is not None

    @property
    def is_hard_deleted(self) -> bool:
        """Vérifie si l'objet est supprimé définitivement"""
        return self.deleted_at is None and self.restored_at is None

    def hard_delete(self, *args, **kwargs):
        """Supprimer définitivement l'objet"""
        super().delete(*args, **kwargs)

    def delete(self, strict: bool = False, *args, **kwargs):
        """Supprimer l'objet"""
        now = timezone.now()
        with transaction.atomic():
            for field in self._meta.get_fields():
                if isinstance(field, GenericRelation):
                    continue
                related_model = field.related_model
                if not related_model:
                    continue
                if strict and not issubclass(related_model, self.__class__):
                    raise SoftDeleteException(f"{related_model.__name__} is not a subclass of SoftDeleteModel.")
                if field.one_to_one:
                    self.__delete_related_one_to_one(field, strict, *args, **kwargs)
                elif field.one_to_many:
                    self.__delete_related_one_to_many(field, strict, *args, **kwargs)
                else:
                    continue
            self.deleted_at = now
            self.restored_at = None
            self.save(
                update_fields=[
                    "deleted_at",
                    "restored_at",
                ]
            )

    def restore(self, strict: bool = True, *args, **kwargs):
        """Restaurer l'objet supprimé"""
        now = timezone.now()
        self.deleted_at = None
        self.restored_at = now
        with transaction.atomic():
            for field in self._meta.get_fields():
                if isinstance(field, GenericRelation):
                    continue
                related_model = field.related_model
                if not related_model:
                    continue
                if strict and not issubclass(related_model, self.__class__):
                    raise SoftDeleteException(f"{related_model.__name__} is not a subclass of SoftDeleteModel.")
                if field.one_to_one:
                    self.__restore_related_one_to_one(field, strict, *args, **kwargs)
                elif field.one_to_many:
                    try:
                        self.__restore_related_one_to_many(field, strict, *args, **kwargs)
                    except ValueError:
                        continue
                else:
                    continue
            self.save(
                update_fields=[
                    "deleted_at",
                    "restored_at",
                ]
            )

    def __delete_related_one_to_one(self, field, strict, *args, **kwargs):
        """Méthode pour supprimer un objet lié en one to one"""
        related_object = getattr(self, field.name, None)
        if related_object:
            remote_model = field.remote_field.model
            related_query_name = field.remote_field.related_query_name or field.remote_field.related_name or field.opts.model_name
            try:
                if hasattr(remote_model, related_query_name):
                    self.__delete_related_object(field, related_object, strict, *args, **kwargs)
            except TypeError:
                pass

    def __delete_related_one_to_many(self, field, strict, *args, **kwargs):
        """Méthode pour supprimer un objet lié en one to many"""
        related_objects = getattr(self, field.get_accessor_name()).all()
        for related_object in related_objects:
            self.__delete_related_object(field, related_object, strict, *args, **kwargs)

    def __restore_related_one_to_one(self, field, strict, *args, **kwargs):
        """Méthode pour restaurer un objet lié en one to one"""

        try:
            related_object = getattr(self, field.name, None)
            if related_object:
                self.__restore_related_object(field, related_object, strict, *args, **kwargs)
        except field.related_model.DoesNotExist:
            pass

    def __restore_related_one_to_many(self, field, strict, *args, **kwargs):
        """Méthode pour restaurer un objet lié en one to many"""

        remote_field = field.remote_field
        remote_model = field.remote_field.model
        if not issubclass(remote_model, self.__class__):
            raise ValueError("No related objects found")
        deleted_objects_manager_name = "deleted_objects"
        filter_criteria = {remote_field.name: self}
        for related_object in getattr(remote_model, deleted_objects_manager_name).filter(**filter_criteria):
            self.__restore_related_object(field, related_object, strict, *args, **kwargs)

    def __delete_related_object(self, field, related_object, strict, *args, **kwargs):
        """Supprimer un objet lié à un objet supprimé"""

        if hasattr(field, "on_delete"):
            on_delete = field.on_delete
        elif hasattr(field, "remote_field") and hasattr(field.remote_field, "on_delete"):
            on_delete = field.remote_field.on_delete
        else:
            return
        if on_delete == models.CASCADE:
            try:
                if strict:
                    kwargs["strict"] = strict
                related_object.delete(*args, **kwargs)
            except related_object.DoesNotExist:
                pass
        elif on_delete == models.SET_NULL:
            setattr(related_object, field.remote_field.name, None)
            related_object.save()
        elif on_delete == models.PROTECT:
            related_query_name = field.remote_field.related_query_name or field.remote_field.related_name or field.opts.model_name
            if callable(related_query_name):
                related_query_name = related_query_name()
            if related_object:
                related_manager_name = related_query_name if hasattr(self, related_query_name) else f"{related_query_name}_set"
                protected_objects = list(getattr(self, related_manager_name).all())
                raise ProtectedError(
                    f"Cannot delete {self} because {related_object} is related with PROTECT",
                    protected_objects=protected_objects,
                )
        elif on_delete == models.SET_DEFAULT:
            default_value = field.get_default()
            setattr(related_object, field.remote_field.name, default_value)
            related_object.save()
        elif on_delete == models.SET:
            if callable(field.remote_field.on_delete_set_function):
                value = field.remote_field.on_delete_set_function(self)
                setattr(related_object, field.remote_field.name, value)
                related_object.save()
        elif on_delete == models.DO_NOTHING:
            pass  # Ne rien faire explicitement
        elif on_delete == models.RESTRICT:
            if related_object:
                raise ProtectedError(
                    f"Cannot delete {self} because {related_object} is related with RESTRICT",
                    [related_object],
                )
        else:  # M2M
            related_object.delete(strict=strict, *args, **kwargs)
        try:
            if related_object.pk is not None:
                related_object.save()
        except AttributeError:
            pass

    def __restore_related_object(self, field, related_object, strict, *args, **kwargs):
        """Restaurer un objet supprimé lié à un objet restauré"""
        if related_object.is_deleted:
            related_object.restore(strict=strict, *args, **kwargs)
            try:
                if related_object.pk is not None:
                    related_object.save()
            except AttributeError:
                pass
