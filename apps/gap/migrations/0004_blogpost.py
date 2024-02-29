# Generated by Django 5.0.2 on 2024-02-27 20:33

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gap', '0003_comment_opinion'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Blog Title')),
                ('body', ckeditor_uploader.fields.RichTextUploadingField()),
            ],
        ),
    ]
