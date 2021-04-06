from django.db import models
from django.urls import reverse

from kreedo.core import TimestampAwareModel
# Create your models here.

class Address(TimestampAwareModel):
    country = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(max_length=200, null=True, blank=True)
    pincode = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=False)