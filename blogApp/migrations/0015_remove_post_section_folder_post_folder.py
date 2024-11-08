# Generated by Django 5.1 on 2024-09-11 07:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogApp', '0014_section_post_section'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='section',
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('parent_folder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subfolders', to='blogApp.folder')),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blogApp.section')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='folder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='files', to='blogApp.folder'),
        ),
    ]
