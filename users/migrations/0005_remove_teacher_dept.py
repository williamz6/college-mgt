# Generated by Django 4.0.5 on 2022-06-19 02:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_teacher_dept'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='dept',
        ),
    ]