# Generated by Django 4.0.5 on 2022-06-23 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_student_dob_alter_teacher_dob_alter_teacher_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='id',
            field=models.CharField(editable=False, max_length=30, primary_key=True, serialize=False),
        ),
    ]