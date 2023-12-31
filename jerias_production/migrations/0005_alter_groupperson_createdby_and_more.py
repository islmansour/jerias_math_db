# Generated by Django 4.0.4 on 2023-07-06 12:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jerias_production', '0004_alter_group_teacherid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupperson',
            name='createdBy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_groupperson', to='jerias_production.person'),
        ),
        migrations.AlterField(
            model_name='groupperson',
            name='lastUpdatedBy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='updated_groupperson', to='jerias_production.person'),
        ),
        migrations.AlterUniqueTogether(
            name='groupperson',
            unique_together={('studentId', 'groupId')},
        ),
    ]
