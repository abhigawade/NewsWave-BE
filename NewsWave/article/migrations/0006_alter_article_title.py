# Generated by Django 5.1.3 on 2025-02-19 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0005_alter_article_author_alter_article_source_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.TextField(),
        ),
    ]
