import bcrypt
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone


class AbstractModel(models.Model):
    id = models.BigIntegerField(primary_key=True, unique=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.id = self.count_records() + 1
            self.created_at = timezone.now()
            self.updated_at = timezone.now()
        else:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    @classmethod
    def count_records(cls):
        try:
            return cls.objects.order_by("id").last().pk
        except AttributeError:
            return 0

    class Meta:
        abstract = True


class BaseModel(models.Model):
    created_at = models.IntegerField(editable=False, null=False)
    updated_at = models.IntegerField(editable=True, null=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = int(timezone.now().timestamp())
        self.updated_at = int(timezone.now().timestamp())
        super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class BaseUserModel(BaseModel, AbstractBaseUser, PermissionsMixin):
    is_staff = models.BooleanField(default=False)
    last_login = None

    def check_password(self, raw_password):
        return bcrypt.checkpw(raw_password.encode(), self.password.encode())

    class Meta:
        abstract = True
