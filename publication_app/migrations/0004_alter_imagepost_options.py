# Generated by Django 4.0.4 on 2022-06-29 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publication_app', '0003_alter_imagepost_post'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='imagepost',
            options={'verbose_name': 'Картинка  поста', 'verbose_name_plural': 'Картинки постов'},
        ),
    ]
