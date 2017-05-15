# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class MyUser(models.Model):
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=16)
    mobilephone = models.CharField(max_length=11)
    permission = models.IntegerField(default=1)
    account = models.FloatField(default=1000.00)

    def __unicode__(self):
        return self.user.username


class Book(models.Model):
    name = models.CharField(max_length=128)
    price = models.FloatField(default=0.00)
    author = models.CharField(max_length=128)
    publish_date = models.DateField()
    category = models.CharField(max_length=128)
    is_allow = models.IntegerField(default=1)
    user_id = models.ForeignKey(User, default=None)

    class META:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Img(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    img = models.ImageField(upload_to='image/%Y/%m/%d/')
    book = models.ForeignKey(Book)

    class META:
        ordering = ['name']

    def __unicode__(self):
        return self.name


# order_seq 表示订单号
# order_num 表示订单数量


class OrderInfo(models.Model):
    order_seq = models.CharField(max_length=15, primary_key=True)
    name = models.CharField(max_length=45)

    order_num = models.IntegerField(default=1)
    price = models.FloatField(default=0.00)
    total_price = models.FloatField(default=0.00)
    my_account = models.FloatField(default=0.00)
    order_date = models.DateTimeField(default=datetime.now)
    book = models.ForeignKey(Book)
    user_name = models.ForeignKey(MyUser, default=None)

    class META:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Admin(models.Model):
    name = models.CharField(max_length=45)

    class META:
        ordering = ['name']

    def __unicode__(self):
        return self.name
