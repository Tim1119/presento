from django.db import models
import uuid 
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models 
from django.utils import timezone 
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManger

class User(AbstractBaseUser,PermissionsMixin):
    pkid = models.BigAutoField(primary_key=True,editable=False)
    id =models.UUIDField(default=uuid.uuid4,editable=False,unique=True)
    full_name= models.CharField(verbose_name=_("Full Name"),max_length=255)
    email = models.EmailField(verbose_name=_('Email'),max_length=255,unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = CustomUserManger()

    class Meta:
        verbose_name = _("Customer Account")
        verbose_name_plural = _("Customer Account")

    def __str__(self):
        return f"Customer account for {self.full_name}"





