from django.contrib import admin
from .models import Location, Session, Customer

# Register your models here.


admin.site.register(Location)
admin.site.register(Session)
admin.site.register(Customer)