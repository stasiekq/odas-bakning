# Generated by Django 5.0.1 on 2024-01-21 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bankapp', '0006_transfer_reciever_name_alter_user_account_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='account_number',
            field=models.CharField(default='317763', max_length=6, unique=True),
        ),
    ]
