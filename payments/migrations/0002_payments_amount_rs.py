# Generated by Django 4.0.4 on 2022-06-07 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payments',
            name='amount_rs',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
