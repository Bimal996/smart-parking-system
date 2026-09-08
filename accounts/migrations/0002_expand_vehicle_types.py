from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="default_vehicle_type",
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
