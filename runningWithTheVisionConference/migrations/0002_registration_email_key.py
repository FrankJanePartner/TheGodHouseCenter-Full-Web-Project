from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("runningWithTheVisionConference", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="registration",
            name="registration_email_key",
            field=models.CharField(editable=False, max_length=64, null=True, unique=True),
        ),
    ]
