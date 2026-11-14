from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Registration",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("firstName", models.CharField(blank=True, max_length=100)),
                ("lastName", models.CharField(blank=True, max_length=100)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("phone", models.CharField(blank=True, max_length=20)),
                ("city", models.CharField(blank=True, max_length=100)),
                (
                    "churchType",
                    models.CharField(blank=True, choices=[("Godhouse", "Godhouse"), ("Others", "Others")], max_length=20),
                ),
                ("godhouseCentre", models.CharField(blank=True, max_length=150)),
                ("otherChurch", models.CharField(blank=True, max_length=150)),
                (
                    "attendanceType",
                    models.CharField(blank=True, choices=[("Physical", "Physical"), ("Virtual", "Virtual")], max_length=10),
                ),
                ("accommodation", models.CharField(blank=True, choices=[("yes", "Yes"), ("no", "No")], max_length=3)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Moment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("caption", models.CharField(max_length=255)),
                ("uploader", models.CharField(max_length=150)),
                ("image", models.ImageField(upload_to="moments/")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
