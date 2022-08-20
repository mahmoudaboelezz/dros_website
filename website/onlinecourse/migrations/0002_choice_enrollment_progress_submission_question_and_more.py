# Generated by Django 4.1 on 2022-08-20 11:08

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("onlinecourse", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Choice",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("choice_text", models.CharField(max_length=200)),
                ("is_correct", models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name="enrollment",
            name="progress",
            field=models.FloatField(default=0.0),
        ),
        migrations.CreateModel(
            name="Submission",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "submission_date",
                    models.DateField(default=django.utils.timezone.now),
                ),
                ("submission_grade", models.FloatField(default=0.0)),
                ("is_graded", models.BooleanField(default=False)),
                ("is_submitted", models.BooleanField(default=False)),
                ("is_correct", models.BooleanField(default=False)),
                ("chocies", models.ManyToManyField(to="onlinecourse.choice")),
                (
                    "enrollment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="onlinecourse.enrollment",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("question_text", models.CharField(max_length=200)),
                ("question_grade", models.FloatField(default=0.0)),
                (
                    "lesson",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="onlinecourse.lesson",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="choice",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="onlinecourse.question"
            ),
        ),
    ]