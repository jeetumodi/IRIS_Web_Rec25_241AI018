from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['equipment', 'infrastructure', 'start_time', 'end_time']
        widgets = {
            'equipment': forms.Select(attrs={'class': 'form-control'}),
            'infrastructure': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        equipment = cleaned_data.get('equipment')
        infrastructure = cleaned_data.get('infrastructure')

        if end_time and start_time:
            if end_time <= start_time:
                self.add_error('end_time', "End time must be after start time.")

        if not equipment and not infrastructure:
            raise ValidationError("A booking must be for either equipment or infrastructure.")

        if equipment and infrastructure:
            raise ValidationError("A booking cannot be for both equipment and infrastructure.")

        # Check for overlapping bookings
        conflicts = Booking.objects.filter(
            start_time__lt=end_time, end_time__gt=start_time
        )
        if equipment:
            conflicts = conflicts.filter(equipment=equipment)
        if infrastructure:
            conflicts = conflicts.filter(infrastructure=infrastructure)

        if conflicts.exists():
            raise ValidationError("This time slot is already booked.")

        return cleaned_data

    def clean_start_time(self):
        start_time = self.cleaned_data.get('start_time')
        if start_time and start_time < timezone.now():
            raise ValidationError("Start time must be in the future.")
        return start_time