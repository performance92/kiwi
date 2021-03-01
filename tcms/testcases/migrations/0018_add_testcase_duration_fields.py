# Generated by Django 3.1.6 on 2021-02-16 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("testcases", "0017_rename_related_names"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicaltestcase",
            name="setup_duration",
            field=models.DurationField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="historicaltestcase",
            name="testing_duration",
            field=models.DurationField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="testcase",
            name="setup_duration",
            field=models.DurationField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="testcase",
            name="testing_duration",
            field=models.DurationField(blank=True, db_index=True, null=True),
        ),
    ]
