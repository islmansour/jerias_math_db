# Generated by Django 4.0.4 on 2023-07-05 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jerias_production', '0003_remove_person_created_remove_person_createdby_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='teacherId',
            field=models.IntegerField(null=True),
        ),
    ]
