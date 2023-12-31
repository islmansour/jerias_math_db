# Generated by Django 4.0.4 on 2023-07-19 05:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jerias_production', '0022_alter_purchase_status_purchaseattendance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='createdBy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='purchases_created', to='jerias_production.person'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='lastUpdatedBy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='purchases_updated', to='jerias_production.person'),
        ),
    ]
