from django.db import models
from django.urls import reverse
from kreedo.core import TimestampAwareModel
from users.models import UserDetail
# Create your models here.

"""  Choice """
Male = 'Male'
Female = 'Female'
Other = 'Other'


Gender_Choice = [
    (Male, 'Male'),
    (Female, 'Female'),
    (Other, 'Other')
]

""" Child Model """


class Child(TimestampAwareModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    type = models.CharField(max_length=25, choices=Gender_Choice)
    date_of_joining = models.DateField()
    place_of_birth = models.CharField(max_length=100, null=True, blank=True)
    blood_group = models.CharField(max_length=100, null=True, blank=True)
    photo = models.CharField(max_length=100, null=True, blank=True)
    parent = models.ManyToManyField(to='users.UserDetail')
    registered_by = models.ForeignKey(
        to='users.UserDetail', on_delete=models.PROTECT)
