from django import template
from django.db.models import Sum
from django.contrib.auth.models import User

from itman.teamstream.models import Project, Work, WorkPeriod, WorkPlan

from datetime import datetime, timedelta

register = template.Library()

@register.inclusion_tag("teamstream/show_period_report.html")
def show_day_summary(date):
    start_of_day = datetime(date.year, date.month, date.day)
    date_range = (start_of_day, start_of_day + timedelta(1) - timedelta(seconds=1))
    return show_period_summary(*date_range)

@register.inclusion_tag("teamstream/show_period_report.html")
def show_period_summary(start, end, projects=None):
    date_range = (start, end)
    
    if projects:
        projects = Project.objects.filter(pk__in=[p.pk for p in projects])
    else:
        projects = Project.objects.all()
    
    projects_id = [p.pk for p in projects]
        
    projects_summary = projects.filter(work__workperiod__start__range=date_range).annotate(hours=Sum("work__workperiod__hours"))
    users_summary = User.objects.filter(workperiod__start__range=date_range, workperiod__work__project__in=projects_id).annotate(hours=Sum("workperiod__hours")).order_by("username")
    
    for user in users_summary:
        user_projects_summary = projects.filter(work__workperiod__start__range=date_range, work__workperiod__user=user).annotate(hours=Sum("work__workperiod__hours"))
        user_projects_summary_dict = {}
        for project_summary in user_projects_summary:
            user_projects_summary_dict[project_summary.pk] = project_summary
        
        all_projects_summary = []
        for project in projects_summary:
            all_projects_summary.append(user_projects_summary_dict.get(project.pk, None))            
        
        user.projects_summary = all_projects_summary
    
    return {"projects_summary": projects_summary,
            "users_summary": users_summary,
            "total_hours": WorkPeriod.objects.filter(start__range=date_range, work__project__in=projects_id).aggregate(hours=Sum("hours"))["hours"],
            "start": start,
            "end": end,
            }
