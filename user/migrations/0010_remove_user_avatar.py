# Generated by Django 2.1.5 on 2019-01-20 16:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_user_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='avatar',
        ),
    ]