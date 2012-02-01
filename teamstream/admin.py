# -*- coding:utf-8 -*-
from django.contrib import admin
from django.template.defaultfilters import floatformat

from itman.teamstream.models import Project, Work, WorkPeriod, WorkPlan
from itman.teamstream.forms import AdminWorkPeriodForm, AdminWorkPlanForm

def hours(instance):
    return floatformat(instance.hours, -2)
hours.admin_order_field = 'hours'

class WorkPeriodAdmin(admin.ModelAdmin):
    list_display = ('user', 'work', 'start', 'end', hours,)
    list_filter = ('user',)
    list_display_links = ('work',)
    list_editable = ('start', 'end',)
    search_fields = ('work__project__name', 'work__title', 'user__username', 'user__first_name', 'user__last_name')
    raw_id_fields = ("work",)

    form = AdminWorkPeriodForm

class WorkPeriodInline(admin.TabularInline):
    model = WorkPeriod
    extra = 1
    
    form = AdminWorkPeriodForm

class WorkAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'project', hours,)
    list_display_links = ('id', 'project',)
    list_filter = ('project',)
    list_editable = ('title',)
    search_fields = ('title', 'project__name',)
    
    inlines = [
        WorkPeriodInline,
    ]

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'trac_url',)
    search_fields = ('name', 'trac_url',)
    search_fields = ('name', 'trac_url',)
    
class WorkPlanAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'project', 'title', 'date', 'show_date',)
    list_filter = ('user', 'project',)
    list_display_links = ('id', 'user',)
    list_editable = ('project', 'title', 'date', 'show_date',)
    search_fields = ('project__name', 'title', 'user__username', 'user__first_name', 'user__last_name')
    
    ordering = ('id',)
    
    form = AdminWorkPlanForm
    
admin.site.register(WorkPeriod, WorkPeriodAdmin)
admin.site.register(Work, WorkAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(WorkPlan, WorkPlanAdmin)
