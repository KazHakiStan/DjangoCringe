# Generated by Django 4.0.4 on 2022-06-27 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('publication_app', '0002_post_file_post_tag_imagepost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagepost',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_images', to='publication_app.post'),
        ),
    ]
