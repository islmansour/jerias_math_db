# Generated by Django 4.0.4 on 2023-07-15 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jerias_production', '0018_person_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='type',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
