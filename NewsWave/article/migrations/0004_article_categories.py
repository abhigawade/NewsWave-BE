# Generated by Django 5.1.3 on 2025-02-12 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_alter_article_author_alter_article_source_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='categories',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]
