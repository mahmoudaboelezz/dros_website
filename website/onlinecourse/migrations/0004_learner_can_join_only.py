# Generated by Django 4.1 on 2022-08-20 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("onlinecourse", "0003_rename_chocies_submission_choices_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="learner",
            name="can_join_only",
            field=models.ManyToManyField(blank=True, to="onlinecourse.course"),
        ),
    ]