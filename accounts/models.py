from django.db import models
import datetime
from django.core.validators import RegexValidator, MaxValueValidator
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
        super().save(*args, **kwargs)
        Profile.objects.get_or_create(user=self, defaults={'bio':None, 'birth_date':None, 'phone':None, 'telegram_id':None})
        return

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile', primary_key=True)
    birth_date = models.DateField(blank=True, null=True)
    # birth_date = models.DateField(blank=True, null=True,
                                    # validators=[MaxValueValidator(datetime.date.today())])
    bio = models.CharField(max_length=1000, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True,
                            validators=[RegexValidator(regex='^09\d{9}$', 
                                                       message='Phone number must be entered in the format: "09123456789". Up to 15 digits allowed.')])
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    telegram_id = models.CharField(max_length=100, blank=True, null=True,
                                    validators=[RegexValidator(regex='^@.+$', message='Telegram ID must start with @')])
    starred_boards = models.ManyToManyField(to='workspaces.Board', related_name='starred_for', blank=True)

    def __str__(self):
        return self.user.username