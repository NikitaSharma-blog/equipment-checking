# Generated by Django 3.0.2 on 2022-03-07 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20220307_0627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_status',
            field=models.IntegerField(choices=[(1, 'Stationary'), (2, 'Upwards'), (3, 'Decline'), (0, 'No_value')], default=0),
        ),
    ]
