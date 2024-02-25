from django.db import models
from autoslug import AutoSlugField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django_quill.fields import QuillField
from apps.profiles.models import Profile

User = get_user_model()


class Tags(models.Model):
    name = models.CharField(max_length=255,unique=True)
    slug = AutoSlugField(populate_from='name', unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Article Tag'
        verbose_name_plural = 'Article Tag'


class Category(models.Model):
    name = models.CharField(max_length=255,unique=True)
    slug = AutoSlugField(populate_from='name', unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Category'



class Article(models.Model):

    class ArticleStatus(models.TextChoices):
        Draft = "Draft", _("Draft")
        Published = "Published", _("Published")

    title= models.CharField(verbose_name=_("Article Title"),max_length=255,unique=True)
    image_headline = models.ImageField(upload_to='headlines-images')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name=_("Article Author"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_("Article Category"))
    tag = models.ManyToManyField(Tags, verbose_name=_("Article Tag"))
    slug = AutoSlugField(populate_from='title', unique=True)
    content = QuillField()
    status = models.CharField(max_length=255, choices=ArticleStatus.choices, default=ArticleStatus.Draft)
    approved = models.BooleanField(default=True)
    likes = models.ManyToManyField(Profile, related_name='liked_articles', blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']
        verbose_name = 'Article'
        verbose_name_plural = 'Article'

    def __str__(self):
        return self.title

    def count_comment(self):
        return self.comment_set.count()

    def get_all_comments(self):
        return self.comment_set.all()

    @property
    def image_headline_url(self):
        try:
            url = self.image_headline.url
        except:
            url = ''
        return url

    def count_likes(self):
        return self.likes.count()

    def toggle_like(self, user_profile):
        if user_profile in self.likes.all():
            self.likes.remove(user_profile)
        else:
            self.likes.add(user_profile)


class Comment(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)  # Assuming Post is your existing model
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
