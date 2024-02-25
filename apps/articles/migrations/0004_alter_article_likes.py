# Generated by Django 5.0.2 on 2024-02-24 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_rename_user_profile_comment_author'),
        ('profiles', '0002_remove_profile_linkedin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_articles', to='profiles.profile'),
        ),
    ]
