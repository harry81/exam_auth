# Generated by Django 4.1.1 on 2022-09-14 01:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ably', '0003_alter_verified_expired_at'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Verified',
            new_name='Verification',
        ),
    ]
