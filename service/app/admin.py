from django.contrib import admin

from .models import VehicleBody, VehicleManufacture, VehicleModel

admin.site.register(VehicleBody)
admin.site.register(VehicleModel)
admin.site.register(VehicleManufacture)
