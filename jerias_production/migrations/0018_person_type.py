# Generated by Django 4.0.4 on 2023-07-15 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jerias_production', '0017_alter_payment_paymenttype'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='type',
            field=models.IntegerField(null=True),
        ),
    ]
