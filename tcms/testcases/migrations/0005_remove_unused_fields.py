# Generated by Django 2.1.5 on 2019-01-19 01:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("testcases", "0004_squashed"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="historicaltestcase",
            name="alias",
        ),
        migrations.RemoveField(
            model_name="historicaltestcase",
            name="is_automated_proposed",
        ),
        migrations.RemoveField(
            model_name="testcase",
            name="alias",
        ),
        migrations.RemoveField(
            model_name="testcase",
            name="is_automated_proposed",
        ),
    ]
