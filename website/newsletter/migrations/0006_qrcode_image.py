# Generated by Django 4.1 on 2022-11-03 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("newsletter", "0005_alter_qrcode_verfication_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="qrcode",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="qrcodes"),
        ),
    ]