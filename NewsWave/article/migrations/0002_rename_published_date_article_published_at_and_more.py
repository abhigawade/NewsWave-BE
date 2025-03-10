# Generated by Django 5.1.3 on 2025-02-10 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='published_date',
            new_name='published_at',
        ),
        migrations.RemoveField(
            model_name='article',
            name='category',
        ),
        migrations.RemoveField(
            model_name='article',
            name='is_translated',
        ),
        migrations.RemoveField(
            model_name='article',
            name='language',
        ),
        migrations.RemoveField(
            model_name='article',
            name='translation_language',
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='url_to_image',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=500),
        ),
    ]
