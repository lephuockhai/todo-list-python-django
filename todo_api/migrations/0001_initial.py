# Generated by Django 4.2.6 on 2023-12-17 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssignInfomation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField()),
                ('list_id', models.BigIntegerField()),
                ('join_user_id', models.BigIntegerField()),
            ],
            options={
                'db_table': 'assigns',
            },
        ),
        migrations.CreateModel(
            name='GroupInfomation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField()),
                ('type', models.CharField(max_length=10)),
                ('parent_id', models.BigIntegerField(null=True, blank=True)),
                ('combined_name', models.CharField(max_length=255)),
                ('order_id', models.IntegerField()),
                ('level', models.IntegerField()),
            ],
            options={
                'db_table': 'groups',
            },
        ),
        migrations.CreateModel(
            name='TaskInfomation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField()),
                ('list_id', models.BigIntegerField()),
                ('create_user_id', models.BigIntegerField()),
                ('assigned_user_id', models.BigIntegerField()),
                ('task_describe', models.TextField(max_length=5000)),
                ('task_status', models.CharField(default='Not Complete', max_length=20)),
                ('due_date', models.DateField()),
                ('order_id', models.AutoField(auto_created=True)),
                ('level', models.IntegerField()),
            ],
            options={
                'db_table': 'tasks',
            },
        ),
    ]
