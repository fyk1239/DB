# Generated by Django 4.1.4 on 2022-12-13 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app01", "0002_remove_announcement_acno_remove_course_ctno_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="teacher",
            name="Tpasswd",
            field=models.CharField(default="123", max_length=20),
        ),
    ]