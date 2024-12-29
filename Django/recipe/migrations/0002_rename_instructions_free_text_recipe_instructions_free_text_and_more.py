# Generated by Django 5.1.4 on 2024-12-29 22:32

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='Instructions_free_text',
            new_name='instructions_free_text',
        ),
        migrations.AlterField(
            model_name='recipe',
            name='id',
            field=models.UUIDField(default=uuid.UUID('0194148d-0311-764d-a0f4-f7b13461105d'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]