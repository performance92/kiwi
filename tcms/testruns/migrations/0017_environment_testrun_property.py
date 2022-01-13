# Generated by Django 3.2.11 on 2022-01-13 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("testruns", "0016_testexecutionproperty"),
    ]

    operations = [
        migrations.CreateModel(
            name="Environment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True)),
                ("description", models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="Property",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("value", models.CharField(max_length=255)),
                (
                    "run",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        to="testruns.testrun",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="EnvironmentProperty",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("value", models.CharField(max_length=255)),
                (
                    "environment",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        to="testruns.environment",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
