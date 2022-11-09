from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    def save(self, *args, **kwargs) -> None:
        if self.is_superuser:
            self.is_active = True
        return super().save(*args, **kwargs)

