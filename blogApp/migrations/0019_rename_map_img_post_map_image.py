# Generated by Django 5.1 on 2024-09-23 09:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogApp', '0018_post_page_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='map_img',
            new_name='map_image',
        ),
    ]