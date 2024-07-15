# Generated by Django 3.2.21 on 2024-06-25 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_customuser_birthdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='previous_abs_difference_eye',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='previous_abs_difference_eyebrows',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='previous_abs_difference_mouth',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='previous_left_eye_area',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='previous_left_eyebrow_distance',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='previous_left_mouth_distance',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='previous_right_eye_area',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='previous_right_eyebrow_distance',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='previous_right_mouth_distance',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
