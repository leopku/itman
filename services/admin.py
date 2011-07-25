from django.contrib import admin
#from itman.services.models import Service, Machine, Location
from itman.services.models import Service, Location, Server, Switch

class ServiceInline(admin.TabularInline):
    model = Service

#class MachineInline(admin.TabularInline):
#    model = Machine
class ServerInline(admin.TabularInline):
    model = Server

class SwitchInline(admin.TabularInline):
    model = Switch

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'kind', )
    list_filter = ('kind', )

class HardwareAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    list_filter = ('location', )
    #inlines = [
    #    ServiceInline,
    #]

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    inlines = [
        ServerInline,
        SwitchInline,
    ]

admin.site.register(Service, ServiceAdmin)
#admin.site.register(Machine, MachineAdmin)
admin.site.register(Server, HardwareAdmin)
admin.site.register(Switch, HardwareAdmin)
admin.site.register(Location, LocationAdmin)
