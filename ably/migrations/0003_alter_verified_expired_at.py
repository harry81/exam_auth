# Generated by Django 4.1.1 on 2022-09-14 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ably', '0002_verified_alter_user_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verified',
            name='expired_at',
            field=models.DateTimeField(null=True),
        ),
    ]
