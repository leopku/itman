# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from polymorphic.polymorphic_model import PolymorphicModel
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Location(models.Model):
    name = models.CharField("名称", max_length=255)
    address = models.CharField("地址", max_length=255, blank=True, null=True)
    phone = models.CharField("紧急电话", max_length=29, blank=True, null=True)
    mobile = models.CharField("手机", max_length=29, blank=True, null=True)
    
    def __unicode__(self):
        return self.name
'''
class BaseEquipment(PolymorphicModel):
    Height_Choices = (
        ('1', '1U'),
        ('2', '2U'),
        ('3', '3U'),
        ('4', '4U'),
    )
    name = models.CharField(verbose_name=_('name'), max_length=255)
    manufacturer = models.CharField(verbose_name=_('manufacturer'), max_length=100, blank=True, null=True)
    height = models.CharField(verbose_name=_('height'), max_length=2, choices=Height_Choices, blank=True, null=True)
    oType = models.CharField(verbose_name=_('oType'), max_length=255, blank=True, null=True)
    location = models.ForeignKey(Location, verbose_name=_('location'), blank=True, null=True)

    def __unicode__(self):
        return self.name
'''

class Hardware(models.Model):
    Height_Choices = (
        ('1', '1U'),
        ('2', '2U'),
        ('3', '3U'),
        ('4', '4U'),
    )
    name = models.CharField('名称', max_length=255)
    manufacturer = models.CharField('生产商', max_length=100, blank=True, null=True)
    height = models.CharField('高度', max_length=2, choices=Height_Choices, blank=True, null=True)
    oType = models.CharField('型号', max_length=255, blank=True, null=True)
    location = models.ForeignKey(Location, verbose_name='位置', blank=True, null=True)

    def __unicode__(self):
        return self.name

class Server(Hardware):
    cpu_type = models.CharField('CPU型号', max_length=50, blank=True, null=True)
    memory = models.SmallIntegerField('内存', blank=True, null=True)
    disk = models.CharField('硬盘', max_length=255, blank=True, null=True)
    is_vm = models.BooleanField('虚拟机', default=False)
        
class Switch(Hardware):
    pass
    
class Port(models.Model):
    
    switch = models.ForeignKey(Switch, verbose_name=_('switch'))
    server = models.ForeignKey(Server, verbose_name=_('server'), blank=True, null=True)
    ip = models.IPAddressField("IP地址", max_length=255, blank=True, null=True)
    
    def __unicode_(self):
        return _(('%s - %s#') % (self.switch.name, self.name))


class Service(models.Model):
    name = models.CharField(verbose_name=_('name'), max_length=255)
    port_number = models.CommaSeparatedIntegerField(verbose_name=_('Ports'), max_length=255)
    domain = models.CharField(verbose_name=_('domain'), max_length=255)
"""
class Service(models.Model):
    Service_Choices = (
        ('Po', 'Port'),
        ('Se', 'Service'),
        ('Do', 'Domain'),
    )
    name = models.CharField("名称", max_length=255)
    kind = models.CharField("类型", max_length=2, choices=Service_Choices)
    ip = models.IPAddressField("IP地址", max_length=255, blank=True, null=True)
    switch = models.ForeignKey(Switch, related_name="switch", blank=True, null=True)
    server = models.ForeignKey(Server, related_name='server', blank=True, null=True)
    
    def __unicode__(self):
        if self.switch:
            return '%s - %s#' % (self.switch.name, self.name)
        else:
            return self.name
"""

# class Comment(models.Model):
#     title = models.CharField(max_length=255)
#     comment = models.TextField()
#     switch = models.ForeignKey(Switch, related_name="switch", blank=True, null=True)
#     server = models.ForeignKey(Server, related_name="server", blank=True, null=True)
#     service = models.ForeignKey(Service, blank=True, null=True)
#     author = models.ForeignKey(User, blank=True, null=True,)
# 
#     def __unicode__(self):
