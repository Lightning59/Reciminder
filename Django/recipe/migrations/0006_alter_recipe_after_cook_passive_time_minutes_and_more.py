# Generated by Django 5.1.4 on 2025-01-17 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0005_recipe_after_cook_passive_time_minutes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='after_cook_passive_time_minutes',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='clean_active_time_minutes',
            field=models.PositiveSmallIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cook_active_time_minutes',
            field=models.PositiveSmallIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cook_passive_time_minutes',
            field=models.PositiveSmallIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='pre_prep_active_time_minutes',
            field=models.PositiveSmallIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='pre_prep_passive_time_minutes',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='prep_active_time_minutes',
            field=models.PositiveSmallIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='total_active_time_minutes',
            field=models.PositiveSmallIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='total_overall_time_minutes',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='total_passive_time_minutes',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
    ]
