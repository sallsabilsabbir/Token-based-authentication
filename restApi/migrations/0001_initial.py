# Generated by Django 5.0.14 on 2025-07-15 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp_id', models.IntegerField()),
                ('emp_name', models.CharField(max_length=25)),
                ('emp_department', models.CharField(max_length=25)),
                ('emp_salarry', models.IntegerField()),
                ('emp_Contact', models.IntegerField()),
                ('emp_address', models.CharField(max_length=20)),
            ],
        ),
    ]
