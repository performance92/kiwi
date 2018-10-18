# Generated by Django 2.1.2 on 2018-10-18 12:21

import datetime
from django.conf import settings
from django.db import migrations, models


def forwards_add_initial_data(apps, schema_editor):
    TestCaseRunStatus = apps.get_model('testruns', 'TestCaseRunStatus')

    TestCaseRunStatus.objects.bulk_create([
        TestCaseRunStatus(name='IDLE', description='', sortkey=1),
        TestCaseRunStatus(name='RUNNING', description='', sortkey=2),
        TestCaseRunStatus(name='PAUSED', description='', sortkey=3),
        TestCaseRunStatus(name='PASSED', description='', sortkey=4),
        TestCaseRunStatus(name='FAILED', description='', sortkey=5),
        TestCaseRunStatus(name='BLOCKED', description='', sortkey=6),
        TestCaseRunStatus(name='ERROR', description='', sortkey=7),
        TestCaseRunStatus(name='WAIVED', description='', sortkey=8),
    ])


def reverse_add_initial_data(apps, schema_editor):
    TestCaseRunStatus = apps.get_model('testruns', 'TestCaseRunStatus')
    status_names = ['IDLE', 'RUNNING', 'PAUSED', 'PASSED', 'FAILED', 'BLOCKED', 'ERROR', 'WAIVED']
    TestCaseRunStatus.objects.filter(name__in=status_names).delete()


def forward_duration_field(apps, schema_editor):
    TestRun = apps.get_model('testruns', 'TestRun')

    for tr in TestRun.objects.all():
        tr.estimated_time_new = datetime.timedelta(seconds=tr.estimated_time)
        tr.save()


def reverse_duration_field(apps, schema_editor):
    TestRun = apps.get_model('testruns', 'TestRun')

    for tr in TestRun.objects.all():
        tr.estimated_time = tr.estimated_time_new.total_seconds()
        tr.save()


class Migration(migrations.Migration):
    atomic = False

    replaces = [
        ('testruns', '0002_add_initial_data'),
        ('testruns', '0003_testrun_estimated_time_remove_max_length'),
        ('testruns', '0004_remove_testrun_errata_id'),
        ('testruns', '0005_alter_testrun_tag'),
        ('testruns', '0007_rename_testbuild_to_build'),
        ('testruns', '0008_rename_env'),
        ('testruns', '0009_rename_testtag'),
        ('testruns', '0010_duration_field'),
        ('testruns', '0011_remove_plan_text_version'),
        ('testruns', '0012_drop_fields_from_testcaserunstatus'),
        ('testruns', '0013_drop_meta_db_name'),
        ('testruns', '0014_historicaltestcaserun')
    ]

    dependencies = [
        ('management', '0002_squashed'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('testruns', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_add_initial_data, reverse_add_initial_data),

        migrations.RemoveField(
            model_name='testrun',
            name='errata_id',
        ),
        migrations.AlterField(
            model_name='testruntag',
            name='run',
            field=models.ForeignKey(on_delete=models.deletion.CASCADE,
                                    related_name='tags', to='testruns.TestRun'),
        ),
        migrations.AlterField(
            model_name='TestCaseRun',
            name='build',
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE, to='management.Build'),
        ),
        migrations.AlterField(
            model_name='TestRun',
            name='build',
            field=models.ForeignKey(on_delete=models.deletion.CASCADE,
                                    related_name='build_run', to='management.Build'),
        ),
        migrations.RenameModel(
            old_name='TCMSEnvRunValueMap',
            new_name='EnvRunValueMap',
        ),
        migrations.AlterField(
            model_name='EnvRunValueMap',
            name='value',
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE, to='management.EnvValue'),
        ),
        migrations.AlterField(
            model_name='TestRun',
            name='env_value',
            field=models.ManyToManyField(
                through='testruns.EnvRunValueMap', to='management.EnvValue'),
        ),
        migrations.AlterField(
            model_name='TestRunTag',
            name='tag',
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE, to='management.Tag'),
        ),
        migrations.AlterField(
            model_name='TestRun',
            name='tag',
            field=models.ManyToManyField(
                related_name='run', through='testruns.TestRunTag', to='management.Tag'),
        ),
        migrations.AddField(
            model_name='testrun',
            name='estimated_time_new',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),

        migrations.RunPython(forward_duration_field, reverse_duration_field),

        migrations.RemoveField(
            model_name='testrun',
            name='estimated_time',
        ),
        migrations.RenameField(
            model_name='testrun',
            old_name='estimated_time_new',
            new_name='estimated_time',
        ),
        migrations.AlterUniqueTogether(
            name='testrun',
            unique_together={('run_id', 'product_version')},
        ),
        migrations.RemoveField(
            model_name='testrun',
            name='plan_text_version',
        ),
        migrations.RemoveField(
            model_name='testcaserunstatus',
            name='auto_blinddown',
        ),
        migrations.RemoveField(
            model_name='testcaserunstatus',
            name='description',
        ),
        migrations.RemoveField(
            model_name='testcaserunstatus',
            name='sortkey',
        ),
        migrations.AlterModelTable(
            name='envrunvaluemap',
            table=None,
        ),
        migrations.AlterModelTable(
            name='testcaserun',
            table=None,
        ),
        migrations.AlterModelTable(
            name='testcaserunstatus',
            table=None,
        ),
        migrations.AlterModelTable(
            name='testrun',
            table=None,
        ),
        migrations.AlterModelTable(
            name='testruncc',
            table=None,
        ),
        migrations.AlterModelTable(
            name='testruntag',
            table=None,
        ),
        migrations.CreateModel(
            name='HistoricalTestCaseRun',
            fields=[
                ('case_run_id', models.IntegerField(blank=True, db_index=True)),
                ('case_text_version', models.IntegerField()),
                ('running_date', models.DateTimeField(blank=True, null=True)),
                ('close_date', models.DateTimeField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('sortkey', models.IntegerField(blank=True, null=True)),
                ('environment_id', models.IntegerField(default=0)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_change_reason', models.TextField(null=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[
                 ('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('assignee', models.ForeignKey(blank=True, db_constraint=False, null=True,
                                               on_delete=models.deletion.DO_NOTHING,
                                               related_name='+', to=settings.AUTH_USER_MODEL)),
                ('build', models.ForeignKey(blank=True, db_constraint=False, null=True,
                                            on_delete=models.deletion.DO_NOTHING,
                                            related_name='+', to='management.Build')),
                ('case', models.ForeignKey(blank=True, db_constraint=False, null=True,
                                           on_delete=models.deletion.DO_NOTHING,
                                           related_name='+', to='testcases.TestCase')),
                ('case_run_status', models.ForeignKey(blank=True, db_constraint=False, null=True,
                                                      on_delete=models.deletion.DO_NOTHING,
                                                      related_name='+',
                                                      to='testruns.TestCaseRunStatus')),
                ('history_user', models.ForeignKey(null=True, on_delete=models.deletion.SET_NULL,
                                                   related_name='+', to=settings.AUTH_USER_MODEL)),
                ('run', models.ForeignKey(blank=True, db_constraint=False, null=True,
                                          on_delete=models.deletion.DO_NOTHING,
                                          related_name='+', to='testruns.TestRun')),
                ('tested_by', models.ForeignKey(blank=True, db_constraint=False, null=True,
                                                on_delete=models.deletion.DO_NOTHING,
                                                related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical test case run',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
    ]
