from django.db import models

# Create your models here.
class Parking(models.Model):
    wing_name = models.CharField(max_length=50)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.wing_name