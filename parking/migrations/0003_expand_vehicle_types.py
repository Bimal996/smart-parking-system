from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("parking", "0002_alter_parkinglot_city"),
    ]

    operations = [
        migrations.AlterField(
            model_name="parkingslot",
            name="vehicle_type",
            field=models.CharField(
                choices=[
                    ("bike", "Bike / Scooter"),
                    ("car", "Car"),
                    ("suv", "SUV / Jeep"),
                    ("van", "Van / Microbus"),
                    ("truck", "Pickup / Truck"),
                ],
                default="car",
                max_length=10,
            ),
        ),
    ]
