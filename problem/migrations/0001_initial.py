# Generated by Django 3.1 on 2022-02-18 02:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utils.common


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('classes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(unique=True)),
                ('description', models.TextField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('data', models.FileField(blank=True, null=True, upload_to=utils.common.upload_to_data)),
                ('solution', models.FileField(blank=True, null=True, upload_to=utils.common.upload_to_solution)),
                ('data_description', models.TextField()),
                ('public', models.BooleanField(default=False)),
                ('evaluation', models.TextField()),
                ('is_deleted', models.BooleanField(default=False)),
                ('class_id', models.ForeignKey(blank=True, db_column='class', null=True, on_delete=django.db.models.deletion.CASCADE, to='classes.class')),
                ('created_user', models.ForeignKey(blank=True, db_column='created_user', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
            options={
                'db_table': 'problem',
            },
        ),
    ]
