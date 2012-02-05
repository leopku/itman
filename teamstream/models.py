# -*- coding:utf-8 -*-

from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from datetime import datetime
from django.core.exceptions import ValidationError
from django.template.defaultfilters import floatformat

from datetime import datetime, timedelta

TODO_DELAY = timedelta(3)

class Project(models.Model):
    """
    Проект.
    """
    
    # Унікальна назва.
    name = models.CharField(max_length=255, unique=True)
    
    # Опціонально урл трака, якщо є потреба генерації урлів наприклад такого виду: #255 перетвориться у http://pleso.net/trac/ticket/255
    # verify_exists виключено бо локально гальмує.
    trac_url = models.URLField(help_text="example: http://dev.pleso.net/trac/", verify_exists=False, blank=True)

    class Meta:
        # Сортуємо по назві
        ordering = ('name',)
        get_latest_by = 'id'
    
    def __unicode__(self):
        return self.name
    
    def delete(self):
        if self.work_set.all().count() > 0 and self.name.find("[trash]") == -1:
            raise ValidationError("Project can be deleted only if its name has '[trash]' OR project is empty.")    
        super(Project, self).delete()
    
class Work(models.Model):
    """
    Робота.
    
    Належить проекту. В межах проекта ідентифікується унікальною назвою.
    """
    
    # Проект, якому належить робота. Не нулл - не складе труднощів зробити проект по дефолту.
    project = models.ForeignKey(Project)
    # Назва (заголовок) роботи - тому така назва філда. Не TextField, щоб це була назва, а не опис.
    title = models.CharField(max_length=255)
    
    # Сумарний час в годинах витрачений на роботу. Автокалькуляція. Денормалізація для спрощення запитів.
    hours = models.FloatField(editable=False, default=0)
    
    class Meta:
        # Використовуємо такий ключ унікальності, щоб групувати роботи по назві та проекту засобами дьянги.
        unique_together = ('project', 'title', )
        # Сортуємо по проектах і порядковому номеру (як тікети).
        ordering = ('-id',)
    
    def __unicode__(self):
        return "%s - %s" % (self.project.name, self.title)
    
    def update_hours(self):
        self.hours = self.workperiod_set.aggregate(hours=Sum('hours'))['hours']
        if self.hours is None:
            self.hours = 0
        self.save()
    
    def delete(self):
        if self.workperiod_set.all().count() > 0 and self.project.name.find("[trash]") == -1:
            raise ValidationError("Work can be deleted only if its project has name '[trash]' in name OR work is empty.")    
        super(Work, self).delete()
    
class WorkPeriodManager(models.Manager):
    
    def close_active_period(self, user):
        active_period = self.get_active_user_period(user)
        if active_period:
            active_period.end = datetime.now()
            active_period.save()
    
    def get_active_user_period(self, user):
        try:
            return WorkPeriod.objects.filter(user=user, end=None).latest()
        except self.model.DoesNotExist:
            return None
    
    def get_last_closed_user_period(self, user):
        try:
            return WorkPeriod.objects.filter(user=user, end__isnull=False).latest()
        except self.model.DoesNotExist:
            return None
    
    def create_work(self, user, project, title, start, end, commit=True):
        try:
            # Шукаємо відкриту роботу з таким заголовком, проектом і початком, щоб закрити його.
            work_period = WorkPeriod.objects.filter(work__title=title,
                                                    work__project=project,
                                                    start=start,
                                                    end=None,
                                                    user=user).latest()
            # Записуємо дату кінця, якщо вона була вказана. Якщо дата кінця нул, а відкритий період знайшовся, то плануємо закрити його поточним часом.
            work_period.end = end is None and datetime.now() or end
        except WorkPeriod.DoesNotExist:
            # Якщо нема що закривати - Створюємо новий період.
            work_period = WorkPeriod(start=start,
                                     end=end, 
                                     user=user)
            # Шукаємо цю роботу, або створюємо нову.
            if commit:
                work, c = Work.objects.get_or_create(project=project, title=title)
                work_period.work = work
        
        if commit:
            work_period.save()
        
        return work_period
    
    def find_conflicting_periods(self, work_period):
        """
        Функція пошуку конфліктів періодів. Включає валідацію, якщо період реверсивний (початок після кінця).
        
        work_period - період, який треба перевірити на конфлікти з іншими.
        """
        
        # Кьюрісет усіх інших періодів даного юзера.
        other_periods = self.exclude(pk=work_period.pk).filter(user=work_period.user)
        
        conflicts = []
        
        # Шукаємо періоди, в які входить дата початку періоду, який треба перевірити.
        closed_confilcts_of_start = other_periods.filter(start__lte=work_period.start, end__gt=work_period.start)
        if closed_confilcts_of_start.count() > 0:
            conflicts.extend(closed_confilcts_of_start)
        
        # Якщо період відкритий, то:
        if work_period.end is None:
            # Шукаємо інші відкриті періоди (спочатку треба закрити всі, щоб відкрити новий).
            open_confilcts = other_periods.filter(end=None)
            if open_confilcts.count() > 0:
                conflicts.extend(open_confilcts)
            
            # Шукаємо закриті періоди, після дати початку даного відкритого.
            open_confilcts = other_periods.filter(end__gt=work_period.start)[:1]
            if open_confilcts.count() > 0:
                conflicts.extend(open_confilcts)
        else:
            # Переівряємо чи кінець не раніше початку.
            if work_period.end < work_period.start:
                raise ValidationError('Work period is reversed.')
            
            # Шукаємо періоди, які містять кінець даної.
            closed_confilcts_of_end = other_periods.filter(start__lte=work_period.end, end__gte=work_period.end)
            if closed_confilcts_of_end.count() > 0:
                conflicts.extend(closed_confilcts_of_end)
            
            # Шукаємо періоди, які виходять всередині даної.
            closed_confilcts_of_inclusion = other_periods.filter(start__gte=work_period.start, end__lte=work_period.end)
            if closed_confilcts_of_inclusion.count() > 0:
                conflicts.extend(closed_confilcts_of_inclusion)
            
            # Шукаємо відкриті періоди, до дати початку даного закритого.
            open_confilcts = other_periods.filter(start__lt=work_period.end, end=None)
            if open_confilcts.count() > 0:
                conflicts.extend(open_confilcts)
        
        # Вертаємо пустий кьюрісет, якщо конфліктів не знайдено.
        return conflicts

class WorkPeriod(models.Model):
    """
    Період виконання роботи. 
    
    У однієї роботи може бути кілька періодів, які показують часові проміжки,
    під час яких вона виконувалась вказаними людьми.
    
    Період роботи може бути відкритий (вказана тільки дата початку), коли дана
    робота робиться зараз. Або період роботи може бути закритий (коли вказана 
    дата початку і дата кінця), коли даний період виконання роботи вже пройшов.
    
    Слід підтримувати базові правила валідації (на рівні форм):
      1. Одна людина не може мати одночасно кілька відкритих періодів робіт. 
      2. Одна людина не може мати два або більше закритих періодів робіт, які
      перетинаються часовим періодом, тобто відбувались одночасно.
      3. Закритий період має мати час завершення, який пізніше час початку.
    """
    
    # Робота, якій належить даний період.
    work = models.ForeignKey(Work)
    # Користувач, що виконує дану роботу під час даного періоду.
    user = models.ForeignKey(User)
    
    # Час початку періоду.    
    start = models.DateTimeField(default=datetime.now)
    # Час завершення періоду. Для відкритих періодів має значення null. Це дозволить зробити просту вибірку по активним/незакритим роботам. Плюс прозоро для логіки.
    end = models.DateTimeField(null=True, blank=True)
    
    # Сумарний час в годинах витрачений на роботу. Автокалькуляція. Денормалізація для спрощення запитів.
    hours = models.FloatField(editable=False, default=0)
    
    objects = WorkPeriodManager()
    
    class Meta:
        ordering = ('-start',)
        get_latest_by = 'start'
    
    def __unicode__(self):
        if self.end:
            return "%s at %s (+%s hours)" % (self.work.title, self.start, floatformat(self.hours, -2))
        else:
            return "%s at %s (opened)" % (self.work.title, self.start)
    
    def save(self, *args, **kwargs):
        # Шукаємо конфліктні періоди. Валідація не для форми, а для цілісності даних.
        conflicting_periods = WorkPeriod.objects.find_conflicting_periods(self)
        if len(conflicting_periods) > 0:        
            raise ValidationError("Conflicts with periods: %s." % ', '.join(unicode(c) for c in conflicting_periods))
        
        if self.end:
            # Визначаємо скільки годин пройшло від початку до кінця. Формула весела, але правильна.
            duration = self.end - self.start
            self.hours = float(duration.days * 24 *60 * 60 + duration.seconds) / (60 * 60) 
        else:
            # Вважаємо що робота ще не має часу, якщо вона незакрита (для простоти). 
            self.hours = 0
        
        original_workperiod = None
        if self.pk:
            old = list(WorkPeriod.objects.filter(pk=self.pk))
            if len(old) > 0:
                original_workperiod = old[0]
            
        super(WorkPeriod, self).save(*args, **kwargs)
        
        if original_workperiod and original_workperiod.work != self.work:
            original_workperiod.work.update_hours()
        
        self.work.update_hours()
        
    
    def delete(self):
        work = self.work
        super(WorkPeriod, self).delete()
        work.update_hours()

class WorkPlan(models.Model):
    """
    План щось зробити. На відміну від типових робіт - не групується (бо нема потреби, звітів на це непотрібно).
    Має проект, власника. Дата початку і дата кінця необов"язкові. Так як буває не знаєш коли почнеш чи закінчиш.
    """
    
    # Користувач, що запланував роботу.
    user = models.ForeignKey(User)
    # Проект, якому належить робота. Не нулл - не складе труднощів зробити проект по дефолту.
    project = models.ForeignKey(Project)
    # Назва (заголовок) роботи - тому така назва філда. Не TextField, щоб це була назва, а не опис.
    title = models.CharField(max_length=255)
    # Планована дата роботи.    
    date = models.DateField(default=(lambda: (datetime.now() + TODO_DELAY).date()))
    # Чи показувати дату плану.
    show_date = models.BooleanField(default=False, help_text="TODOs have this option unchecked")
    
    def is_delayed_todo(self):
        return not self.show_date and self.date < datetime.now().date()
    
    def is_future_plan(self):
        return self.show_date and self.date > datetime.now().date()
            
    class Meta:
        ordering = ('date', 'id')
        get_latest_by = 'id'
    
    def __unicode__(self):
        return "%s (%s)" % (self.title, self.date)