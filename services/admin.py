from django.contrib import admin
from django.contrib import comments
from itman.services.models import Service, Location, Server, Switch

from django import forms

"""
class xheditor(forms.Textarea):
    class Media:
        js = ('/static/xheditor/jquery/jquery-1.4.2.min.js', '/static/xheditor/xheditor-1.1.8-zh-cn.min.js', )
    
    def __init__(self, attrs={}):
        attrs['class'] = "xheditor {skin:'nostyle', tools:'Source,|,Cut,Copy,Paste,Pastetext,|,Blocktag,Fontface,FontSize,Bold,Italic,Underline,Strikethrough,FontColor,BackColor,|,SelectAll,Removeformat,|,Align,List,Outdent,Indent,|,Link,Unlink,Anchor,Hr,Table,Preview'}"
        super(xheditor, self).__init__(attrs)

class ServiceModelAdminForm(forms.ModelForm):
    pass
    class Meta:
        model = Service
        widgets = {
            'name': xheditor()
        }

class ServiceModelAdmin(admin.ModelAdmin):
    form  = ServiceModelAdminForm
"""

class CommentInline(admin.TabularInline):
    model = comments.models.Comment

class ServiceInline(admin.TabularInline):
    model = Service

class ServerInline(admin.TabularInline):
    model = Server

class SwitchInline(admin.TabularInline):
    model = Switch

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'port_number', 'domain', )
    #list_filter = ('kind', 'switch', 'server',)

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

#admin.site.register(Service, ServiceModelAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Server, HardwareAdmin)
admin.site.register(Switch, HardwareAdmin)
admin.site.register(Location, LocationAdmin)
