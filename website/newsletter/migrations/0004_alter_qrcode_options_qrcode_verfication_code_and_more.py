# Generated by Django 4.1 on 2022-11-02 19:55

from django.conf import settings
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("calendarapp", "0003_alter_event_id_alter_eventmember_id"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("newsletter", "0003_alter_qrcode_qr_code"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="qrcode",
            options={"verbose_name": "QR Code", "verbose_name_plural": "QR Codes"},
        ),
        migrations.AddField(
            model_name="qrcode",
            name="verfication_code",
            field=models.UUIDField(
                blank=True, default=uuid.uuid4, editable=False, null=True, unique=True
            ),
        ),
        migrations.AlterUniqueTogether(
            name="qrcode",
            unique_together={("user", "event")},
        ),
    ]