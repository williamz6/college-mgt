# Generated by Django 4.0.5 on 2022-07-11 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0021_course_shortname'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='class',
            options={'verbose_name_plural': 'classes'},
        ),
    ]