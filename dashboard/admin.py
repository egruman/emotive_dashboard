# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Dialogue, Customer

admin.site.register(Dialogue)
admin.site.register(Customer)

# Register your models here.
