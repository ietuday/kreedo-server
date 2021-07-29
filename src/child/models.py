from activity.models import*
from django.db import models
from django.urls import reverse
from kreedo.core import TimestampAwareModel
from users.models import *
from schools.models import *
from session.models import *
from django.contrib.postgres.fields import JSONField
from .managers import*
from plan.models import*
# Create your models here.


"""  Relationship Choice """
Individual = 'Individual'
Group = 'Group'


Academic_Session_Type_Choice = [
    (Individual, 'Individual'),
    (Group, 'Group')
]


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
    gender = models.CharField(max_length=25, choices=Gender_Choice,null=True, blank=True)
    date_of_joining = models.DateField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=100, null=True, blank=True)
    blood_group = models.CharField(max_length=100, null=True, blank=True)
    photo = models.CharField(max_length=100, null=True, blank=True)
    parent = models.ManyToManyField(to='users.UserDetail', blank=True)
    registered_by = models.ForeignKey(
        to='users.UserDetail', on_delete=models.PROTECT, related_name='registered_by', null=True, blank=True)
    reason_for_discontinue = models.TextField(null=True, blank=True)
    school =  models.ForeignKey(
        to='schools.School', on_delete=models.PROTECT, null=True, blank=True, related_name='child_school')
    class_teacher =  models.ForeignKey(
        to='users.UserDetail', on_delete=models.PROTECT,null=True, related_name='child_class_teacher',blank=True)
    account_manager =  models.ForeignKey(
        to='users.UserDetail', on_delete=models.PROTECT,related_name='child_account_manager',null=True, blank=True)
    
    is_active = models.BooleanField(default=False)
    secret_pin = models.CharField(max_length=50, default='0000')

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
    residence_details = JSONField(blank=True, null=True)
    emergency_contact_details = JSONField(null=True, blank=True)
    siblings = JSONField(null=True, blank=True)
    documents = JSONField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'ChildDetail'
        verbose_name_plural = 'ChildDetails'
        ordering = ['-id']

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('ChildDetail_detail', kwargs={"pk": self.pk})



""" Child Session Model """


class ChildSession(TimestampAwareModel):
    child = models.ForeignKey(
        'Child', on_delete=models.CASCADE, null=True, blank=True)
    session_name = models.CharField(max_length=100, null=True, blank=True)
    session_type = models.CharField(
        max_length=50, choices=Academic_Session_Type_Choice)
    academic_session = models.ForeignKey(
        to='session.AcademicSession', on_delete=models.PROTECT, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'ChildSession'
        verbose_name_plural = 'ChildSessions'
        ordering = ['-id']
        # unique_together = ['child','session_type','is_active']

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('ChildSession_detail', kwargs={"pk": self.pk})


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
        unique_together = ['academic_session','attendance_date']

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('Attendance_detail', kwargs={"pk": self.pk})


""" Block Model """


class Block(TimestampAwareModel):
    block_no = models.CharField(max_length=100, null=True, blank=True)
    child_plan = models.ForeignKey(
        to='plan.ChildPlan', on_delete=models.PROTECT, null=True, blank=True)
    activity = models.ForeignKey(
        to='activity.Activity', on_delete=models.PROTECT, null=True, blank=True)
    is_done = models.BooleanField(default=False)
    period = models.ForeignKey(
        to='period.Period', on_delete=models.PROTECT, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Block'
        verbose_name_plural = 'Blocks'
        ordering = ['-id']

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('Block_detail', kwargs={"pk": self.pk})
