from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings
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

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile', primary_key=True)
    birth_date = models.DateField(blank=True, null=True)
    bio = models.CharField(max_length=1000, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True,
                            validators=[RegexValidator(regex='^09\d{9}$', 
                                                       message='Phone number must be entered in the format: "09123456789". Up to 15 digits allowed.')])
    profile_pic = models.URLField(max_length=1000, blank=True, null=True)
    telegram_id = models.CharField(max_length=100, blank=True, null=True,
                                    validators=[RegexValidator(regex='^@.+$', message='Telegram ID must start with @')])

