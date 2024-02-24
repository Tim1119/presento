from django.db import models
from django.contrib.auth import get_user_model
from autoslug import AutoSlugField
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

User= get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('User'))
    avatar = ProcessedImageField(upload_to='avatars', processors=[ResizeToFill(100, 100)], format='JPEG', options={'quality': 60})
    bio = models.TextField(verbose_name=_('Bio'), default='bio')
    instagram = models.URLField(verbose_name=_('Instagram'), blank=True, null=True)
    twitter = models.URLField(verbose_name=_('Twitter'), blank=True, null=True)
    facebook = models.URLField(verbose_name=_('Facebook'), blank=True, null=True)
    slug = AutoSlugField(populate_from='user', unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    @property
    def profile_pic_url(self):
        try:
            url = self.avatar.url
        except:
            url = ''
        return url

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profile'

    def __str__(self):
        return self.user.full_name
