# Generated by Django 4.0.4 on 2023-07-16 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jerias_production', '0019_alter_person_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='account_owner_data', to='jerias_production.person'),
        ),
    ]
