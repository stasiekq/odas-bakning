# Generated by Django 5.0.1 on 2024-01-19 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bankapp', '0004_alter_user_account_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transfer',
            old_name='reciepent',
            new_name='reciever',
        ),
        migrations.AlterField(
            model_name='user',
            name='account_number',
            field=models.CharField(default='896381', max_length=6, unique=True),
        ),
    ]