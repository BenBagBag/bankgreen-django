# Generated by Django 4.0.5 on 2022-06-11 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brand', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentary',
            name='our_take',
            field=models.TextField(blank=True, help_text='Positive. used to to give our take on green banks'),
        ),
    ]