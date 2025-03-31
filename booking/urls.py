from django.urls import path
from .views import book_equipment,booking_success,booking_unsuccess,user_bookings

urlpatterns = [
    path('user_bookings/',user_bookings,name='user_bookings'),
    path('book/', book_equipment, name='book_equipment'),
    path('booking_success/',booking_success, name='booking_success'),
    path('booking_unsuccess',booking_unsuccess, name='booking_unsuccess')
]
