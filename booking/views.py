from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils.timezone import now
from django.utils.dateparse import parse_datetime
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Booking, Equipment, Infrastructure
from .forms import BookingForm

@login_required
def book_equipment(request):
    error_message = None
    form = BookingForm()

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            equipment = form.cleaned_data.get('equipment')
            infrastructure = form.cleaned_data.get('infrastructure')
            start_time = form.cleaned_data.get('start_time')
            end_time = form.cleaned_data.get('end_time')
            time_difference = end_time - start_time
            booking_date = start_time.date()  # Extract only the date (YYYY-MM-DD)

            # Prevent same user from booking another equipment or infrastructure on the same day
            existing_user_booking = Booking.objects.filter(
                user=request.user,
                start_time__date=booking_date  # Compare only the date part
            ).exists()

            if existing_user_booking:
                error_message = "You already have a booking on this day. You cannot book another equipment or infrastructure."
                print(f"Error message set: {error_message}")
                return render(request, 'booking_unsuccess.html', {'error_message': error_message})

            # Equipment Booking Validation
            if equipment:
                if equipment.maintenance_status == 'Under Maintenance' or not equipment.is_available:
                    error_message = f"{equipment.name} is not available or under maintenance."
                    print(f"Error message set: {error_message}")
                    return render(request, 'booking_unsuccess.html', {'error_message': error_message})

                # Prevent booking conflicts
                existing_booking = Booking.objects.filter(
                    equipment=equipment,
                    start_time__lt=end_time,
                    end_time__gt=start_time
                ).exists()
                if existing_booking:
                    error_message = "The selected equipment is already booked for this time slot."
                    return render(request, 'booking_unsuccess.html', {'error_message': error_message})

                # Prevent equipment bookings exceeding 4 hours
                if time_difference.total_seconds() > 14400:  # 4 hours max
                    error_message = "You can book an equipment only for a maximum of 4 hours."
                    return render(request, 'booking_unsuccess.html', {'error_message': error_message})

            # Infrastructure Booking Validation
            if infrastructure:
                if not infrastructure.is_available:
                    error_message = "Current infrastructure is not available."
                    return render(request, 'booking_unsuccess.html', {'error_message': error_message})

                # Prevent booking conflicts
                existing_booking = Booking.objects.filter(
                    infrastructure=infrastructure,
                    start_time__lt=end_time,
                    end_time__gt=start_time
                ).exists()

                if existing_booking:
                    error_message = "The selected infrastructure is already booked for this time slot."
                    print(error_message)
                    return render(request, 'booking_unsuccess.html', {'error_message': error_message})

                # Prevent infrastructure bookings exceeding 1 hour
                if time_difference.total_seconds() > 3600:  # 1 hour max
                    error_message = "You can book an infrastructure only for a maximum of 1 hour."
                    print(error_message)
                    return render(request, 'booking_unsuccess.html', {'error_message': error_message})

            # Save the Booking
            booking = form.save(commit=False)
            booking.user = request.user
            print("Saving booking:", booking)
            booking.save()
            print("Booking saved successfully!")

            return redirect('booking_success')

    return render(request, 'booking_form.html', {'form': form, 'error_message': error_message})

@login_required
def booking_success(request):
    return render(request, 'booking_success.html')

@login_required
def booking_unsuccess(request):
    return render(request, 'booking_unsuccess.html', {'error_message': request.GET.get('error_message', '')})

@login_required
def user_bookings(request):
    bookings = Booking.objects.filter(user=request.user)  # Fetch only the logged-in user's bookings
    return render(request, 'user_bookings.html', {'bookings': bookings})