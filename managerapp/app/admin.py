from django.contrib import admin
from .models import User, Venue, Menu, Service, FoodItem
# Register your models here.

admin.site.register(User)
admin.site.register(Menu)
admin.site.register(Venue)
admin.site.register(Service)
admin.site.register(FoodItem)