# Generated by Django 4.0.4 on 2023-07-11 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jerias_production', '0012_purchase_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='jerias_production.account'),
        ),
    ]