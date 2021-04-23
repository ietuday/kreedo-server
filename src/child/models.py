from django.db import models
from django.urls import reverse
from kreedo.core import TimestampAwareModel
from users.models import *
from schools.models import *
from session.models import *
from django.contrib.postgres.fields import JSONField
from .managers import*

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


""" Session_With_Kreedo_Choice """
Kreedo = 'Kreedo'
New = 'New'

Session_With_Kreedo_Choice = [
    (Kreedo, 'Kreedo'),
    (New, 'New')
]

""" Child Model """


class Child(TimestampAwareModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=25, choices=Gender_Choice)
    date_of_joining = models.DateField()
    place_of_birth = models.CharField(max_length=100, null=True, blank=True)
    blood_group = models.CharField(max_length=100, null=True, blank=True)
    photo = models.CharField(max_length=100, null=True, blank=True)
    parent = models.ManyToManyField(to='users.UserDetail', blank=True)
    registered_by = models.ForeignKey(
        to='users.UserDetail', on_delete=models.PROTECT, related_name='registered_by', null=True, blank=True)

    reason_for_discontinue = models.TextField(null=True, blank=True)

    is_active = models.BooleanField(default=False)
    objects = ChildManager

    class Meta:
        verbose_name = 'Child'
        verbose_name_plural = 'Childs'
        ordering = ['-id']

    def __str__(self):
        return str(self.first_name)

    def get_absolute_url(self):
        return reverse('Child_detail', {"pk": self.pk})


""" child detail Model """


class ChildDetail(TimestampAwareModel):
    child = models.ForeignKey('Child', on_delete=models.CASCADE)
    medical_details = JSONField(blank=True, null=True)
    recidence_details = JSONField(blank=True, null=True)
    emergency_of_contact_details = JSONField()
    siblings_details = JSONField(null=True, blank=True)
    document_checklist = JSONField()
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'ChildDetail'
        verbose_name_plural = 'ChildDetails'
        ordering = ['-id']

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('ChildDetail_detail', kwargs={"pk": self.pk})


""" Attendance Model """


class Attendance(TimestampAwareModel):
    academic_session = models.ForeignKey(
        to='session.AcademicSession', on_delete=models.PROTECT)
    marked_status = models.BooleanField(default=False)
    childs = JSONField(blank=True, null=True)
    attendance_date = models.DateField(null=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendances'
        ordering = ['-id']

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('Attendance_detail', kwargs={"pk": self.pk})
