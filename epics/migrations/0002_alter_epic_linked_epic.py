# Generated by Django 3.2.12 on 2022-02-14 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('epics', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='epic',
            name='linked_epic',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='epic', to='epics.epic'),
        ),
    ]
