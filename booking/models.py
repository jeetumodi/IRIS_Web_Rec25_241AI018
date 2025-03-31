from django.db import models
from django.contrib.auth.models import User

# Equipment Model
class Equipment(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    maintenance_status = models.CharField(
        max_length=20,
        choices=[('Available', 'Available'), ('Under Maintenance', 'Under Maintenance')],
        default='Available'
    )

    def __str__(self):
        return self.name

# Infrastructure Model
class Infrastructure(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# Booking Model
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.SET_NULL, null=True, blank=True)
    infrastructure = models.ForeignKey(Infrastructure, on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')],
        default='Pending'
    )
    def __str__(self):
        return f"{self.user.username} - {self.equipment or self.infrastructure} ({self.status})"
