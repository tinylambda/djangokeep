# Generated by Django 4.1.1 on 2022-09-22 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("basedata", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="projecttype",
            name="remarks",
        ),
        migrations.RemoveField(
            model_name="projecttype",
            name="standard_price",
        ),
    ]
