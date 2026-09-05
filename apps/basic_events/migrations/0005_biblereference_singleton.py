from django.db import migrations, models


def consolidate_bible_references(apps, schema_editor):
    reference_model = apps.get_model("basic_events", "BibleReference")
    references = list(reference_model.objects.order_by("id"))

    if not references:
        return

    primary_reference = references[0]
    reference_model.objects.exclude(pk=primary_reference.pk).delete()

    if primary_reference.pk != 1:
        reference_model.objects.filter(pk=primary_reference.pk).update(pk=1)


def restore_bible_references(apps, schema_editor):
    # The singleton migration intentionally removes duplicate Bible references.
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("basic_events", "0004_about_singleton"),
    ]

    operations = [
        migrations.RunPython(consolidate_bible_references, restore_bible_references),
        migrations.AlterField(
            model_name="biblereference",
            name="id",
            field=models.PositiveSmallIntegerField(
                default=1,
                editable=False,
                primary_key=True,
                serialize=False,
            ),
        ),
    ]
