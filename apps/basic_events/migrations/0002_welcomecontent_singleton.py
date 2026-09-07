from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("basic_events", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="welcomecontent",
            name="id",
            field=models.PositiveSmallIntegerField(
                default=1,
                editable=False,
                primary_key=True,
                serialize=False,
            ),
        ),
    ]