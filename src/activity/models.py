from django.db import models
from django.urls import reverse
from kreedo.core import TimestampAwareModel
from users.models import*
from schools.models import*

# Create your models here.

"""  Relationship Choice """
Individual = 'Individual'
Group = 'Group'


Activity_Type_Choice = [
    (Individual, 'Individual'),
    (Group, 'Group')
]


""" Activity Model """


class Activity(TimestampAwareModel):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50, choices=Activity_Type_Choice)
    objective = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    notes = models.CharField(max_length=200, blank=True, null=True)
    subject = models.ManyToManyField(to='schools.Subject', blank=True)
    # skill = models.ManyToManyField(to='skill', blank=True)
    created_by = models.ForeignKey(
        to='users.UserDetail', on_delete=models.PROTECT)
    duration = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Activity'
        verbose_name_plural = 'Activitys'
