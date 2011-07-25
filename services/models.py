# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Location(models.Model):
    name = models.CharField("名称", max_length=255)
    address = models.CharField("地址", max_length=255, blank=True, null=True)
    phone = models.CharField("紧急电话", max_length=29, blank=True, null=True)
    mobile = models.CharField("手机", max_length=29, blank=True, null=True)
    
    def __unicode__(self):
        return self.name

class Service(models.Model):
    Service_Choices = (
        ('Po', 'Port'),
        ('Se', 'Service'),
        ('Do', 'Domain'),
    )
    name = models.CharField("名称", max_length=255)
    kind = models.CharField("类型", max_length=2, choices=Service_Choices)
    ip = models.IPAddressField("IP地址", max_length=255, blank=True, null=True)
    #machine = models.ForeignKey(Hardware, verbose_name="机器", blank=True, null=True)
    #hardware = models.ManyToManyField(Hardware, verbose_name='机器', blank=True, null=True)
    
    def __unicode__(self):
        return self.name
        #return '%s - %s' % (self.hardware_set.all()[0].name, self.name)
        #return '%s - %s' % (self.hardware_set.get(port=self), self.name)

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
    port = models.ManyToManyField(Service, verbose_name='端口', limit_choices_to={'kind__exact': 'Po'})

    def __unicode__(self):
        return self.name

class Server(Hardware):
    cpu_type = models.CharField('CPU型号', max_length=50, blank=True, null=True)
    memory = models.SmallIntegerField('内存', blank=True, null=True)
    disk = models.CharField('硬盘', max_length=255, blank=True, null=True)
    #port = models.ManyToManyField(Service, limit_choices_to={'kind__exact': 'Po'})

class Switch(Hardware):
    #port = models.ManyToManyField(Service, limit_choices_to={'kind__exact': 'Po'})
    pass
# class Machine(models.Model):
#     Machine_Choices = (
#         ('Se', 'Server'),
#         ('Sw', 'Switch'),
#     )
#     Height_Choices = (
#         ('1U', '1U'),
#         ('2U', '2U'),
#         ('3U', '3U'),
#         ('4U', '4U'),
#         ('5U', '5U'),
#     )
#     name = models.CharField("名称", max_length=255)
#     manufacturer = models.CharField("生产商", max_length=100)
#     height = models.CharField("高度", max_length=2, choices=Height_Choices)
#     mType = models.CharField("型号", max_length=255, )
#     kind = models.CharField("类型", max_length=2, choices=Machine_Choices)
#     disk = models.CharField("硬盘", max_length=100, blank=True, null=True)
#     memory = models.CharField("内存", max_length=20, blank=True, null=True)
#     location = models.ForeignKey(Location, blank=True, null=True)
#     
#     def __unicode__(self):
#         return self.name


