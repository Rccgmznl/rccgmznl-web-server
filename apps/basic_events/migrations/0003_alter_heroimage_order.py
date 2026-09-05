from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("basic_events", "0002_about"),
    ]

    operations = [
        migrations.AlterField(
            model_name="heroimage",
            name="order",
            field=models.PositiveIntegerField(unique=True),
        ),
    ]