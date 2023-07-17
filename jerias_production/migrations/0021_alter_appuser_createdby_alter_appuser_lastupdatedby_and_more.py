# Generated by Django 4.0.4 on 2023-07-16 09:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jerias_production', '0020_alter_account_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='createdBy',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_appuser', to='jerias_production.person'),
        ),
        migrations.AlterField(
            model_name='appuser',
            name='lastUpdatedBy',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_appuser', to='jerias_production.person'),
        ),
        migrations.AlterField(
            model_name='appuser',
            name='person',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='jerias_production.person'),
        ),
        migrations.AlterField(
            model_name='group',
            name='createdBy',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_group', to='jerias_production.person'),
        ),
        migrations.AlterField(
            model_name='group',
            name='lastUpdatedBy',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_group', to='jerias_production.person'),
        ),
        migrations.AlterField(
            model_name='group',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='group_teacher', to='jerias_production.person'),
        ),
        migrations.AlterField(
            model_name='groupevent',
            name='createdBy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_events', to='jerias_production.person'),
        ),
        migrations.AlterField(
            model_name='groupevent',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='jerias_production.group'),
        ),
        migrations.AlterField(
            model_name='groupevent',
            name='lastUpdatedBy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_events', to='jerias_production.person'),
        ),
        migrations.AlterField(
            model_name='groupperson',
            name='createdBy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_groupperson', to='jerias_production.person'),
        ),
        migrations.AlterField(
            model_name='groupperson',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='group_people', to='jerias_production.group'),
        ),
        migrations.AlterField(
            model_name='groupperson',
            name='lastUpdatedBy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_groupperson', to='jerias_production.person'),
        ),
        migrations.AlterField(
            model_name='groupperson',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='group_participations', to='jerias_production.person'),
        ),
    ]
