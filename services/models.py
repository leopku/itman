# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class Service(models.Model):
    Service_Choices = (
        ('Po', 'Port'),
        ('Se', 'Service'),
        ('Do', 'Domain'),
    )
    name = models.CharField("名称", max_length=255)
    kind = models.CharField("类型", max_length=2, choices=Service_Choices)
    ip = models.IPAddressField("IP地址", max_length=255, null=True)
    

class Machine(models.Model):
    Machine_Choices = (
        ('Se', 'Server'),
        ('Sw', 'Switch'),
    )
    name = models.CharField("名称", max_length=255)
    port = models.CommaSeparatedIntegerField("端口", max_length=4)
    services = models.CommaSeparatedIntegerField("服务", max_length=255, null=True)
    kind = models.CharField("类型", max_length=2, choices=Machine_Choices)
    location = models.ForeignKey(Location)

class Location(models.Model):
    name = models.CharField("名称", max_length=255)
    address = models.CharField("地址", max_length=255)
    phone = models.CharField("紧急电话", max_length=29, null=True)
    mobile = models.CharField("手机", max_length=29, null=True)