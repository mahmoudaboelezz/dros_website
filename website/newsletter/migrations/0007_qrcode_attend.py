# Generated by Django 4.1 on 2022-11-03 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("newsletter", "0006_qrcode_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="qrcode",
            name="attend",
            field=models.BooleanField(default=False),
        ),
    ]
