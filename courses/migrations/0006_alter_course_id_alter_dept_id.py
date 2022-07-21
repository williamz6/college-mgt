# Generated by Django 4.0.5 on 2022-06-19 02:18

from django.db import migrations
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_alter_course_options_alter_dept_options_class'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='id',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='abcdefg1234567890*$@', length=8, max_length=16, prefix='id_', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='dept',
            name='id',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='abcdefg1234567890*$@', length=8, max_length=16, prefix='id_', primary_key=True, serialize=False),
        ),
    ]