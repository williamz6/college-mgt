# Generated by Django 4.0.5 on 2022-10-16 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_attendancerange_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancerange',
            name='end_date',
            field=models.DateField(default='2022-10-19'),
        ),
        migrations.AlterField(
            model_name='attendancerange',
            name='start_date',
            field=models.DateField(default='2022-10-17'),
        ),
    ]