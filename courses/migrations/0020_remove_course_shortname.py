# Generated by Django 4.0.5 on 2022-06-26 18:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0019_alter_college_name_alter_dept_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='shortname',
        ),
    ]