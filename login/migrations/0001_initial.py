# Generated by Django 2.2.3 on 2020-05-06 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='', max_length=200)),
                ('action', models.CharField(default='', max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('day', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
