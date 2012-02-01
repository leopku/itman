# -*- coding:utf-8 -*-

from django import forms
from django.contrib.admin.widgets import AdminSplitDateTime, AdminRadioSelect, AdminDateWidget

from itman.teamstream.models import Project, Work, WorkPeriod, WorkPlan, TODO_DELAY

from datetime import datetime, timedelta

class ReportParamsForm(forms.Form):
    date = forms.DateField(required=False,
                           initial=datetime.now().date,
                           widget=AdminDateWidget)
    days = forms.IntegerField(required=False,
                              min_value=1, 
                              initial=datetime.now().isoweekday())
    projects = forms.ModelMultipleChoiceField(required=False,
                                              queryset=Project.objects.all())
    draft = forms.BooleanField(required=False)

class StripTitle:
    def clean_title(self):
        title = self.cleaned_data['title']
        if title:
            title = title.strip()
        return title    

class ForbidFutureScheduleWorkPeriod:
    
    def validate_not_future(self, date):
        if date is not None and date > datetime.now():
            raise forms.ValidationError("You can't schedule work activity to the future. Specify current or past time or use plan instead.")
        return date
    
    def clean_start(self):
        return self.validate_not_future(self.cleaned_data['start'])
    
    def clean_end(self):
        return self.validate_not_future(self.cleaned_data['end'])

class AdminWorkPeriodForm(forms.ModelForm, ForbidFutureScheduleWorkPeriod, StripTitle):
    
    def clean(self):
        """
        Валідатор для адмінської форми.
        """
        # Якщо заголовок або проект відсутні - нема як валідувати.
        if 'work' not in self.cleaned_data or 'user' not in self.cleaned_data:
            return self.cleaned_data
        
        if 'start' in self.cleaned_data and self.cleaned_data['start']:
            start = self.cleaned_data['start']
        else:
            return self.cleaned_data
            
        if 'end' in self.cleaned_data and self.cleaned_data['end']:
            end = self.cleaned_data['end']
        else:
            end = None
        
        if 'id' in self.cleaned_data and self.cleaned_data['id']:
            id = self.cleaned_data['id'].pk
        elif self.instance.pk:
            id = self.instance.pk
        else:
            id = None
            
        if start and end:
            # Якщо кінець вказаний, то валідумєо чи він правильний
            if end < start:
                raise forms.ValidationError("Period start must be earlier than end.")
        else:
            end = None
        
        try:
            # Шукаємо відкриту роботу по ід.
            work_period = WorkPeriod.objects.get(pk=id)
        except WorkPeriod.DoesNotExist:
            # Якщо нема що закривати - створюємо новий період. Не записуємо - тільки для валідації.
            work_period = WorkPeriod(user=self.cleaned_data['user'])
        
        work_period.start = start
        work_period.end = end
        
        # Перевірка на конфліктуючі періоди.
        conflicting_periods = WorkPeriod.objects.find_conflicting_periods(work_period)
        if len(conflicting_periods) > 0:
            raise forms.ValidationError("Conflicts with periods: %s." % ', '.join(unicode(c) for c in conflicting_periods))
        return self.cleaned_data
    
    class Meta:
        model = WorkPeriod

class UserCustomWorkForm(forms.Form, ForbidFutureScheduleWorkPeriod, StripTitle):
    """
    Спеціальна форма додавання роботи з періодом її виконання.
    
    Вміє створити нову роботу і прив"язати до неї час. При цьому період може бути як закритим так і відкритим.
    Вміє підв"язати новий період часу до існуючої роботи, якщо вже є така в даному проекті.
    Вміє закрити по часу вже існуючий відкритий період роботи.
    Проводить валідацію періоду, щоб не було конфліктів з іншими.
    Ініціалізує форму останньою діяльністю даного юзера. 
    """
    
    project = Work._meta.get_field('project').formfield(empty_label=None, widget=AdminRadioSelect(attrs={'class': 'radiolist'}))
    title = Work._meta.get_field('title').formfield()
    
    start = forms.SplitDateTimeField(help_text="Leave empty to start new work",
                                     required=False,
                                     initial=None,
                                     widget=AdminSplitDateTime)
    end = forms.SplitDateTimeField(help_text="If start specified - leave empty to close work with current time.",
                                   required=False,
                                   initial=None,
                                   widget=AdminSplitDateTime)
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        
        work_period = None
        
        work_period = WorkPeriod.objects.get_active_user_period(self.user)
        if work_period is not None:
            # Пробуємо загрузити останню відкриту діяльність юзера.
            work_period = WorkPeriod.objects.filter(end=None,
                                                    user=self.user).latest()
            # Беремо з неї проект, заголовок і початок.
            initial = {'project': work_period.work.project.pk,
                       'title': work_period.work.title,
                       'start': work_period.start}
        else:
            work_period = WorkPeriod.objects.get_last_closed_user_period(self.user)
            if work_period is not None:
                # Якщо нема відкритої - шукаємо закриту. 
                work_period = WorkPeriod.objects.filter(user=self.user).latest()
                # Беремо з неї проект.
                initial = {'project': work_period.work.project.pk}
            else:
                # Інакше загружаємо останій проект або створюємо дефолтовий.
                try:
                    project = Project.objects.all().latest()
                except Project.DoesNotExist:
                    project = Project(name='default')
                    project.save()
                initial = {'project': project.pk}
        
        super(UserCustomWorkForm, self).__init__(initial=initial, *args, **kwargs)
    
    def clean(self):
        # Якщо заголовок або проект відсутні - нема як валідувати.
        if 'title' not in self.cleaned_data or 'project' not in self.cleaned_data:
            return self.cleaned_data
        
        if 'start' in self.cleaned_data and self.cleaned_data['start']:
            start = self.cleaned_data['start']
        else:
            # Якщо початок не вказаний, то ініціалізуємо поточним часом. Такий спосіб, бо сторінка з ініціалізованим часом може висіти довго і є ймовірність записати роботу раніше ніж треба.
            start = datetime.now()
            
        if 'end' in self.cleaned_data and self.cleaned_data['end']:
            end = self.cleaned_data['end']
        else:
            end = None
            
        if start and end:
            # Якщо кінець вказаний, то валідумєо чи він правильний
            if end < start:
                raise forms.ValidationError("Period start must be earlier than end.")
        else:
            end = None
        
        work_period = WorkPeriod.objects.create_work(self.user, self.cleaned_data['project'], self.cleaned_data['title'], start, end, commit=False)
        
        # Перевірка на конфліктуючі періоди.
        conflicting_periods = WorkPeriod.objects.find_conflicting_periods(work_period)
        if len(conflicting_periods) > 0:
            raise forms.ValidationError("Conflicts with periods: %s." % ', '.join(unicode(c) for c in conflicting_periods))
        
        return self.cleaned_data
    
    def save(self):
        if self.cleaned_data['start']:
            start = self.cleaned_data['start']
        else:
            # Якщо початок не вказаний, то ініціалізуємо поточним часом. Такий спосіб, бо сторінка з ініціалізованим часом може висіти довго і є ймовірність записати роботу раніше ніж треба.
            start = datetime.now()
            
        if 'end' in self.cleaned_data: 
            end = self.cleaned_data['end'] 
        else:
            end = None
        
        WorkPeriod.objects.create_work(self.user, self.cleaned_data['project'], self.cleaned_data['title'], start, end)

class AdminWorkPlanForm(forms.ModelForm, StripTitle):
    
    class Meta:
        model = WorkPlan
    
class UserCustomWorkPlanForm(AdminWorkPlanForm, StripTitle):
    
    project = WorkPlan._meta.get_field('project').formfield(empty_label=None, widget=AdminRadioSelect(attrs={'class': 'radiolist'}))
    title = WorkPlan._meta.get_field('title').formfield()
    
    date = forms.DateField(required=False,
                           initial=None,
                           widget=AdminDateWidget)
    
    plan_marker = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    
    class Meta:
        model = WorkPlan
        exclude = ("user", "show_date")
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        
        try:
            # Загружаємо останній створений юзером план.
            work_plan = WorkPlan.objects.filter(user=self.user).latest()
            # Беремо з ннього проект.
            initial = {'project': work_plan.project.pk}
        except WorkPlan.DoesNotExist:
            # Інакше загружаємо останій проект або створюємо дефолтовий.
            try:
                project = Project.objects.all().latest()
            except Project.DoesNotExist:
                project = Project(name='default')
                project.save()
            initial = {'project': project.pk}
                        
        super(UserCustomWorkPlanForm, self).__init__(initial=initial, *args, **kwargs)
    
    def clean_date(self):
        date = self.cleaned_data['date']
        if date is not None and date < datetime.now().date():
            raise forms.ValidationError("You can't schedule work finish to the past. Specify future time or leave empty.")
        return date
    
    def save(self):
        work_plan = super(UserCustomWorkPlanForm, self).save(commit=False)
        work_plan.user = self.user
        
        if work_plan.date is None:
            work_plan.date = (datetime.now() + TODO_DELAY).date()
        else:
            work_plan.show_date = True
        
        work_plan.save()
        return work_plan
