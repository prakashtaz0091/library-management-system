# Generated by Django 5.0.6 on 2024-06-02 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='mobile_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
