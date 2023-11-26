from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# model named giving for storing user's giving info such as first name, last name, email, chosen giving type, currency and amount
class Profile(models.Model):
    giving_type = (
        ('offering', 'offering'), 
        ('tithe', 'tithe')
        ("teacher's send", "teacher's send")
        ('special giving', 'special giving')
        )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    type = models.SmallIntegerField(choices=giving_type)
    amount = models.DecimalField(decimal_places=2, max_digits=15)

    def __str__(self):
        return f'{self.user.username} ${self.amount}'
    