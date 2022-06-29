# Generated by Django 4.0.4 on 2022-06-22 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tags_app', '0001_initial'),
        ('media_app', '0001_initial'),
        ('publication_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='file',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='media_app.media'),
        ),
        migrations.AddField(
            model_name='post',
            name='tag',
            field=models.ManyToManyField(blank=True, related_name='tag_post', to='tags_app.tag'),
        ),
        migrations.CreateModel(
            name='ImagePost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='posts/%Y')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imageposts', to='publication_app.post')),
            ],
            options={
                'verbose_name': 'Фотография  поста',
                'verbose_name_plural': 'Фотограции постов',
            },
        ),
    ]
