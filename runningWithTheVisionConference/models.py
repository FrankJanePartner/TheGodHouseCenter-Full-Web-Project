from django.db import models

class Registration(models.Model):
    CHURCH_TYPE_CHOICES = [
        ("Godhouse", "Godhouse"),
        ("Others", "Others"),
    ]

    ATTENDANCE_TYPE_CHOICES = [
        ("Physical", "Physical"),
        ("Virtual", "Virtual"),
    ]

    ACCOMMODATION_CHOICES = [
        ("yes", "Yes"),
        ("no", "No"),
    ]

    firstName = models.CharField(max_length=100, blank=True)
    lastName = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)

    churchType = models.CharField(max_length=20, choices=CHURCH_TYPE_CHOICES, blank=True)
    godhouseCentre = models.CharField(max_length=150, blank=True)
    otherChurch = models.CharField(max_length=150, blank=True)

    attendanceType = models.CharField(max_length=10, choices=ATTENDANCE_TYPE_CHOICES, blank=True)
    accommodation = models.CharField(max_length=3, choices=ACCOMMODATION_CHOICES, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.firstName} {self.lastName}"


class Moment(models.Model):
    caption = models.CharField(max_length=255)
    uploader = models.CharField(max_length=150)
    image = models.ImageField(upload_to="moments/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.caption
