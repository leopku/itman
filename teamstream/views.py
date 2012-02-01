# -*- coding:utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.db.models import Sum

from itman.teamstream.forms import UserCustomWorkForm, UserCustomWorkPlanForm, ReportParamsForm
from itman.teamstream.models import Project, Work, WorkPeriod, WorkPlan, TODO_DELAY

from itman.lib.decorators import basic_auth_required, simple_basic_auth_callback

from datetime import datetime, timedelta

DEFAULT_LAST_ACTIVITY_DAYS_COUNT = 3

def get_plans_context(request):
    filter = request.session.get("plans_filter", "all")
    
    now = datetime.now()
    
    if filter == "my":
        all_plans = WorkPlan.objects.filter(user=request.user).select_related('project')
    else:
        all_plans = WorkPlan.objects.all().select_related('project')
        filter == "all"
    
    # Майбутні плани - мають дату більше поточної
    future_plans = all_plans.filter(date__gt=now.date(), show_date=True)
    # Плани на сьогодні.
    today_plans = all_plans.filter(date=now.date(), show_date=True)
    # Завершені плани - мають дату кінця, яка вже відбулась.
    past_plans = all_plans.filter(date__lt=now.date(), show_date=True)
    
    # активні.
    general_plans = all_plans.filter(date__gte=now.date(), show_date=False)
    # застарілі.
    delayed_plans = all_plans.filter(date__lt=now.date(), show_date=False)
    
    return {"future_plans" : future_plans,
            "today_plans" : today_plans,
            "past_plans": past_plans,
            "general_plans" : general_plans,
            "delayed_plans" : delayed_plans,
            "now": now,
            "filter": filter,
           }

@basic_auth_required(realm='Team Stream', callback_func=simple_basic_auth_callback)
def main(request):
    form = UserCustomWorkForm(user=request.user)
    plan_form = UserCustomWorkPlanForm(user=request.user, auto_id="id_plan_%s")
        
    if request.method == "POST":
        if "plan_marker" in request.POST:
            plan_form = UserCustomWorkPlanForm(user=request.user, data=request.POST)
            if plan_form.is_valid():
                plan_form.save()
                return HttpResponseRedirect(reverse("main"))
        else:
            form = UserCustomWorkForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse("main"))
    
    now = datetime.now()
    
    start_date = datetime(now.year, now.month, now.day) - timedelta(DEFAULT_LAST_ACTIVITY_DAYS_COUNT - 1)
    # Останні активності.
    last_activities = WorkPeriod.objects.filter(start__gte=start_date, end__isnull=False).select_related("work__project")
    # Відкриті активності.
    current_activities = WorkPeriod.objects.filter(end__isnull=True).select_related("work__project")
    
    context = {"form": form,
               "plan_form": plan_form,
               "activities": last_activities,
               "current_activities": current_activities,
               "now": now,}
    
    plans_context = get_plans_context(request)
    context.update(plans_context)    
    
    return render_to_response("teamstream/index.html",
                              context, context_instance=RequestContext(request))

@basic_auth_required(realm='Close activity period', callback_func=simple_basic_auth_callback)
def report(request, project_id=None):
    date = datetime.now().date()
    days = datetime.now().isoweekday()
    projects = []
    draft = False
    
    if len(request.GET):
        form = ReportParamsForm(request.GET)
        if form.is_valid():
            date = form.cleaned_data["date"] and form.cleaned_data["date"] or date
            days = form.cleaned_data["days"] and form.cleaned_data["days"] or days
            projects = form.cleaned_data["projects"] and form.cleaned_data["projects"] or []
            draft = form.cleaned_data["draft"]
    else:
        form =  ReportParamsForm()
    
    start_of_end_day = datetime(date.year, date.month, date.day)
    
    start_date = start_of_end_day - timedelta(days - 1)
    end_date = start_of_end_day + timedelta(1) - timedelta(seconds=1)
    
    date_range = (start_date, 
                  end_date)
    
    if projects:
        projects = Project.objects.filter(pk__in=[p.pk for p in projects])
    else:
        projects = Project.objects.all()
        
    projects = projects.filter(work__workperiod__start__range=date_range).annotate(hours=Sum("work__workperiod__hours"))
    
    for project in projects:
        project.works = Work.objects.filter(workperiod__work__project=project, workperiod__start__range=date_range).annotate(hours=Sum("workperiod__hours")).select_related('project').order_by("title")
        
        project.users = User.objects.filter(workperiod__work__project=project, workperiod__start__range=date_range).annotate(hours=Sum("workperiod__hours")).order_by("username")
        for user in project.users:
            user.works = Work.objects.filter(workperiod__work__project=project, workperiod__user=user, workperiod__start__range=date_range).annotate(hours=Sum("workperiod__hours")).select_related('project').order_by("title")
    
    return render_to_response(draft and "teamstream/report_draft.html" or "teamstream/report.html",
                              {"form": form,
                               "projects": projects,
                               "start": start_date,
                               "end": end_date,
                               }, context_instance=RequestContext(request))

def ajax_show_plans(request):
    filter = request.GET.get("filter", None)
    if filter is not None:
        request.session["plans_filter"] = filter
    return render_to_response("teamstream/show_plans.html",
                              get_plans_context(request), context_instance=RequestContext(request))
    

@basic_auth_required(realm='Close activity period', callback_func=simple_basic_auth_callback)
def close_active_period(request):
    WorkPeriod.objects.close_active_period(request.user)
    return HttpResponseRedirect(request.GET.get("next", reverse("main")))

@basic_auth_required(realm='Resume activity', callback_func=simple_basic_auth_callback)
def resume_work(request, id):
    work = get_object_or_404(Work, pk=id)
    WorkPeriod.objects.close_active_period(request.user)
    WorkPeriod(work=work, user=request.user, start=datetime.now()).save()
    return HttpResponseRedirect(request.GET.get("next", reverse("main")))

@basic_auth_required(realm='Delete plan', callback_func=simple_basic_auth_callback)
def delete_plan(request, id):
    work_plan = get_object_or_404(WorkPlan, pk=id)
    if work_plan.user != request.user:
        return HttpResponseForbidden()
    work_plan.delete()
    return HttpResponseRedirect(request.GET.get("next", reverse("main")))

@basic_auth_required(realm='Delete period', callback_func=simple_basic_auth_callback)
def delete_period(request, id):
    work_period = get_object_or_404(WorkPeriod, pk=id)
    if work_period.user != request.user:
        return HttpResponseForbidden()
    work = work_period.work
    work_period.delete()
    if work.workperiod_set.all().count() == 0:
        work.delete()        
    return HttpResponseRedirect(request.GET.get("next", reverse("main")))

@basic_auth_required(realm='Delete plan', callback_func=simple_basic_auth_callback)
def ajax_delete_plan(request):
    id = request.POST.get("id", None)
    work_plan = get_object_or_404(WorkPlan, pk=id)
    if work_plan.user != request.user:
        return HttpResponseForbidden()
    work_plan.delete()
    return HttpResponse("ok")

@basic_auth_required(realm='Delay plan', callback_func=simple_basic_auth_callback)
def ajax_delay_plan(request):
    id = request.POST.get("id", None)
    try:
        days = int(request.POST.get("days", 1))
    except TypeError:
        days = 1
    work_plan = get_object_or_404(WorkPlan, pk=id)
    if work_plan.user != request.user:
        return HttpResponseForbidden()
    
    if days == 0:
        # Якщо 0 - значить це рефреш тудушки.
        work_plan.date = datetime.now().date() + TODO_DELAY
    else:
        # Сунемо заплановану дату події вперед відносно поточного дня, або відносно дня події, якщо вона ще не відбулась.
        base_date = work_plan.date > datetime.now().date() and work_plan.date or datetime.now().date()
        work_plan.date = base_date + timedelta(days)
        # Якщо це була тудушка - то це зробить її планом.s
        work_plan.show_date = True
        
    work_plan.save()
    return HttpResponse("ok")

@basic_auth_required(realm='Resume activity', callback_func=simple_basic_auth_callback)
def resume_plan(request, id):
    work_plan = get_object_or_404(WorkPlan, pk=id)
    WorkPeriod.objects.close_active_period(request.user)
    try:
        work = Work.objects.get(project=work_plan.project, title=work_plan.title)
    except Work.DoesNotExist:
        work = Work(project=work_plan.project, title=work_plan.title)
        work.save()
    WorkPeriod(work=work, user=request.user, start=datetime.now()).save()
    return HttpResponseRedirect(request.GET.get("next", reverse("main")))
