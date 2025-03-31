from django.contrib import admin
from .models import Equipment
from .models import Infrastructure
from .models import Booking


admin.site.register(Equipment) 
admin.site.register(Infrastructure)
admin.site.register(Booking)
