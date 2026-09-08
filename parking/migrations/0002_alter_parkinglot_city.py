from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("parking", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="parkinglot",
            name="city",
            field=models.CharField(
                choices=[("dhangadhi", "Dhangadhi")],
                max_length=20,
            ),
        ),
    ]
