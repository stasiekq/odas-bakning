# Generated by Django 5.0.1 on 2024-01-19 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bankapp', '0003_rename_reciever_transfer_reciepent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='account_number',
            field=models.CharField(default='953885', max_length=6, unique=True),
        ),
    ]
