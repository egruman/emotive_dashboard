# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Customer(models.Model):
    first_name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    product_type = models.CharField(max_length=20)

    def __str__(self):
       return "Customer "+str(self.id)

class Dialogue(models.Model):
    greeting = models.CharField(max_length=500)
    if_pos = models.CharField(max_length=500)
    if_neg = models.CharField(max_length=500)

    @staticmethod
    def default():
        return Dialogue(greeting="Hi <firstName>, I saw that <productType> was delivered.  How are you enjoying it so far?",
                        if_pos="Great, can you describe what you love most about <productType>?",
                        if_neg="I'm sorry to hear that, what did you dislike about <productType>?")

    def __str__(self):
       return "Dialogue "+str(self.id)
