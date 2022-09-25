# Generated by Django 4.1.1 on 2022-09-22 09:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("basedata", "0002_remove_projecttype_remarks_and_more"),
        ("vendor", "0004_alter_vendor_desired_project_type"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="vendor",
            name="desired_project_type",
        ),
        migrations.CreateModel(
            name="VendorPrice",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "price_standard",
                    models.PositiveIntegerField(verbose_name="standard price"),
                ),
                (
                    "price_inferred",
                    models.PositiveIntegerField(verbose_name="inferred price"),
                ),
                ("date_updated", models.DateTimeField(auto_now=True)),
                ("date_added", models.DateTimeField(auto_now_add=True)),
                (
                    "project_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="basedata.projecttype",
                    ),
                ),
                (
                    "vendor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="vendor.vendor",
                    ),
                ),
            ],
            options={
                "unique_together": {("vendor", "project_type")},
            },
        ),
    ]
