# Generated by Django 4.0.5 on 2022-06-01 23:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teacher',
            old_name='namse',
            new_name='name',
        ),
    ]
