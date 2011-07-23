from django.contrib import admin
from itman.services.models import Service, Machine, Location

class ServiceInline(admin.TabularInline):
    model = Service

class MachineInline(admin.TabularInline):
    model = Machine

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'kind', 'machine')
    list_filter = ('kind', 'machine')

class MachineAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    list_filter = ('location', )
    inlines = [
        ServiceInline,
    ]

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    inlines = [
        MachineInline,
    ]

admin.site.register(Service, ServiceAdmin)
admin.site.register(Machine, MachineAdmin)
admin.site.register(Location, LocationAdmin)
