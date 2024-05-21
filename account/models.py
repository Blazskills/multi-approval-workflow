import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Permission
from account.managers import CustomUserManager
# from core_apps.vendor.models import Vendor


class User(AbstractBaseUser, PermissionsMixin):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(verbose_name=_("first name"), max_length=50)
    last_name = models.CharField(verbose_name=_("last name"), max_length=50)

    username = models.CharField(
        verbose_name=_("username"), max_length=50, db_index=True, unique=True
    )
    email = models.EmailField(
        verbose_name=_(" Personal email"),
        db_index=True,
        help_text=" Personal email address",
    )
    user_photo = models.ImageField(
        upload_to="user/photos/",
        verbose_name=_("user photo"),
        blank=True,
        null=True,
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

    user_type = models.CharField(
        max_length=50,
        choices=[("vc", "VC"),
                 ("dvc", "DVC"),
                 ("registrar", "Registrar"),
                 ("dean", "Dean"),
                 ("hod", "HOD"),
                 ("lecturer", "Lecturer")],
    )
    temp_verification_link = models.URLField(null=True, blank=True)

    # TODO: Pending implementation
    temp_password = models.CharField(max_length=60, blank=True)
    initial_password_changed = models.BooleanField(default=False)
    initial_password_changed_at = models.DateTimeField(blank=True, null=True)

    date_joined = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    date_deleted = models.DateTimeField(auto_now=True, null=True)

    USERNAME_FIELD = "username"

    REQUIRED_FIELDS = ["first_name", "last_name", "email"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ("-created", "-updated")

    def __str__(self):
        return f"{self.username.title()} {self.first_name.title()} {self.user_type.title()}"

    def get_user_permissions_list(self):
        try:
            perms = Permission.objects.filter(
                content_type__app_label=User._meta.app_label,
                content_type__model=User._meta.model_name,
                user=self,
            ).order_by("codename")
            return list(set([x.codename for x in perms]))
        except Exception as e:
            print(e)
            return []

    @property
    def get_full_name(self):
        return f"{self.first_name.title()} {self.last_name.title()}"

    @property
    def get_short_name(self):
        return self.first_name

    @property
    def get_user_permissions_codenames(self):
        try:
            perms = Permission.objects.filter(
                content_type__app_label=User._meta.app_label,
                content_type__model=User._meta.model_name,
                user=self,
            ).order_by("codename")
            listp = list(set([x.codename for x in perms]))
        except Exception as e:
            print(e)
            listp = []
        return ",".join(listp)

    @property
    def get_user_roles(self):
        return (str(self.get_user_permissions_codenames)).replace("_", " ").title()

    def get_all_permissions(self, obj=None):
        """
        :return: The list of permission codename from both groups and perms
        """
        for perm in super().get_all_permissions(obj=obj):
            yield perm.split(".")[1]

    @property
    def all_user_permissions_display(self):
        return ", ".join(self.get_all_permissions()).replace("_", " ").title()

    @property
    def user_groups(self):
        group_list = self.groups.values_list("name", flat=True)
        return ", ".join(group_list).replace("_", " ").title()
