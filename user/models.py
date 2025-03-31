from django.db import models
from django.contrib.auth.models import User
import os
from django.utils.timezone import now
from django.core.validators import RegexValidator

def user_profile_picture_path(instance, filename):
    """
    Upload profile pictures to 'profile_pics/user_<id>/filename'
    """
    ext = filename.split('.')[-1]
    filename = f"profile_{now().strftime('%Y%m%d%H%M%S')}.{ext}"
    return os.path.join(f"profile_pics/user_{instance.user.id}/", filename)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(
        max_length=15, 
        blank=True, 
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', "Enter a valid phone number.")]
    )
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to=user_profile_picture_path, default="profile_pics/default.jpg")

    def __str__(self):
        return self.user.username

class OtherData(models.Model):  # Renamed to PascalCase
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credits = models.PositiveSmallIntegerField()
    CGPA = models.DecimalField(max_digits=4, decimal_places=2)
    semester = models.CharField(max_length=3)  # Fixed spelling mistake

    def __str__(self):
        return self.user.username
