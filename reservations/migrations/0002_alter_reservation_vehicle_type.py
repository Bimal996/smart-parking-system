from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("parking", "0003_expand_vehicle_types"),
        ("reservations", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reservation",
            name="vehicle_type",
            field=models.CharField(
                choices=[
                    ("bike", "Bike / Scooter"),
                    ("car", "Car"),
                    ("suv", "SUV / Jeep"),
                    ("van", "Van / Microbus"),
                    ("truck", "Pickup / Truck"),
                ],
                max_length=10,
            ),
        ),
    ]
