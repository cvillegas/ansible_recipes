# Generated by Django 3.0.5 on 2020-04-04 03:50

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.encoder
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="TermsAcceptance",
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
                    "terms_type",
                    models.CharField(
                        blank=True,
                        max_length=64,
                        null=True,
                        verbose_name="Tipo de versión",
                    ),
                ),
                (
                    "terms_version",
                    models.CharField(
                        blank=True, max_length=64, null=True, verbose_name="Versión"
                    ),
                ),
                (
                    "ip_address",
                    models.GenericIPAddressField(
                        blank=True, null=True, verbose_name="Dirección IP"
                    ),
                ),
                (
                    "request_context",
                    jsonfield.fields.JSONField(
                        blank=True,
                        dump_kwargs={
                            "cls": jsonfield.encoder.JSONEncoder,
                            "separators": (",", ":"),
                        },
                        load_kwargs={},
                        null=True,
                        verbose_name="Contexto de la solicitud",
                    ),
                ),
                (
                    "object_id",
                    models.PositiveIntegerField(verbose_name="ID del objeto"),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Fecha y hora de creación"
                    ),
                ),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="pageview_counters",
                        to="contenttypes.ContentType",
                        verbose_name="Tipo de contenido",
                    ),
                ),
            ],
            options={
                "verbose_name": "aceptación de términos y condiciones",
                "verbose_name_plural": "aceptaciones de términos y condiciones",
            },
        ),
    ]