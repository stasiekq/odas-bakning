# Generated by Django 5.0.1 on 2024-01-19 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bankapp', '0002_alter_sensitivedata_credit_card_number_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transfer',
            old_name='reciever',
            new_name='reciepent',
        ),
        migrations.AlterField(
            model_name='user',
            name='account_number',
            field=models.CharField(default='944643', max_length=6, unique=True),
        ),
    ]
