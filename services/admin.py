from django.contrib import admin
from itman.services.models import Service, Location, Server, Switch

class ServiceInline(admin.TabularInline):
    model = Service

class ServerInline(admin.TabularInline):
    model = Server

class SwitchInline(admin.TabularInline):
    model = Switch

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'kind', 'switch', )
    list_filter = ('kind', 'switch', 'server',)

class HardwareAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'manufacturer', 'height', 'oType')
    list_filter = ('location', 'manufacturer', 'height', 'oType')
    inlines = [
        ServiceInline,
    ]

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    inlines = [
        ServerInline,
        SwitchInline,
    ]

admin.site.register(Service, ServiceAdmin)
admin.site.register(Server, HardwareAdmin)
admin.site.register(Switch, HardwareAdmin)
admin.site.register(Location, LocationAdmin)
