# Generated by Django 4.0.1 on 2022-01-13 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_authgroup_authgrouppermissions_authpermission_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='N_Category',
            fields=[
                ('c_id', models.AutoField(primary_key=True, serialize=False)),
                ('c_name', models.CharField(max_length=5, unique=True)),
            ],
            options={
                'db_table': 'N_category',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='N_CategoryDetail',
            fields=[
                ('cd_id', models.AutoField(primary_key=True, serialize=False)),
                ('cd_name', models.CharField(max_length=10, unique=True)),
            ],
            options={
                'db_table': 'N_category_detail',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='N_content',
            fields=[
                ('nc_id', models.AutoField(primary_key=True, serialize=False)),
                ('n_content', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'N_content',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='N_summarization',
            fields=[
                ('ns_id', models.AutoField(primary_key=True, serialize=False)),
                ('ns_content', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'N_summarization',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='AuthGroup',
        ),
        migrations.DeleteModel(
            name='AuthGroupPermissions',
        ),
        migrations.DeleteModel(
            name='AuthPermission',
        ),
        migrations.DeleteModel(
            name='AuthUser',
        ),
        migrations.DeleteModel(
            name='AuthUserGroups',
        ),
        migrations.DeleteModel(
            name='AuthUserUserPermissions',
        ),
        migrations.DeleteModel(
            name='DjangoAdminLog',
        ),
        migrations.DeleteModel(
            name='DjangoContentType',
        ),
        migrations.DeleteModel(
            name='DjangoMigrations',
        ),
        migrations.DeleteModel(
            name='DjangoSession',
        ),
        migrations.DeleteModel(
            name='NCategory',
        ),
        migrations.DeleteModel(
            name='NCategoryDetail',
        ),
        migrations.DeleteModel(
            name='NContent',
        ),
        migrations.DeleteModel(
            name='NSummarization',
        ),
        migrations.DeleteModel(
            name='PyboNCategory',
        ),
        migrations.DeleteModel(
            name='PyboNCategoryDetail',
        ),
        migrations.DeleteModel(
            name='PyboNContent',
        ),
        migrations.DeleteModel(
            name='PyboNews',
        ),
        migrations.DeleteModel(
            name='PyboNSummarization',
        ),
        migrations.DeleteModel(
            name='PyboPress',
        ),
    ]
