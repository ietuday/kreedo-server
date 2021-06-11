from django.db import models
from django.urls import reverse
from kreedo.core import TimestampAwareModel
from .managers import*
from schools.models import*
from period.models import*
from users.models import*
# Create your models here.

"""  Relationship Choice """
Individual = 'Individual'
Group = 'Group'


Academic_Session_Type_Choice = [
    (Individual, 'Individual'),
    (Group, 'Group')
]


class SchoolSession(TimestampAwareModel):
    school = models.ForeignKey(to='schools.School', on_delete=models.PROTECT)
    year = models.DateField(blank=True)
    session_from = models.DateField(blank=True)
    session_till = models.DateField(blank=True)
    is_current_session = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    objects = SchoolSessionManager

    class Meta:
        verbose_name = 'SchoolSession'
        verbose_name_plural = 'SchoolSessions'
        ordering = ['-id']

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('SchoolSession_detail', kwargs={"pk": self.pk})

""" Year according Calender Genration """
class SchoolCalendar(TimestampAwareModel):
    school = models.ForeignKey(to='schools.School', on_delete=models.PROTECT)
    session = models.CharField(max_length=50, null=True, blank=True)
    session_from = models.DateField(blank=True)
    session_till = models.DateField(blank=True)
    is_active = models.BooleanField(default=False)
    

    class Meta:
        verbose_name = 'SchoolCalendar'
        verbose_name_plural = 'SchoolCalendars'
        ordering = ['-id']

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('SchoolCalendar_detail', kwargs={"pk": self.pk})



"""  Academic Session Model """


class AcademicSession(TimestampAwareModel):
    name = models.CharField(max_length=50, null=True, blank=True)
    session = models.ForeignKey('SchoolSession', on_delete=models.PROTECT, null=True, blank=True)
    grade = models.ForeignKey(to='schools.Grade', on_delete=models.PROTECT, null=True, blank=True)
    section = models.ForeignKey(to='schools.Section', on_delete=models.PROTECT, null=True, blank=True)
    Subject = models.ManyToManyField(to='schools.Subject')
    type = models.CharField(
        max_length=50, choices=Academic_Session_Type_Choice)
    school_calender = models.ForeignKey('SchoolCalendar', on_delete=models.PROTECT, null=True, blank=True)
    session_from = models.DateField(blank=True)
    session_till = models.DateField(blank=True)
    period_template = models.ForeignKey(
        to='period.PeriodTemplate', on_delete=models.PROTECT, null=True, blank=True)
    class_teacher = models.ForeignKey(
        to='users.UserDetail', on_delete=models.PROTECT)
    academic_calender = models.ForeignKey(
        'AcademicCalender', on_delete=models.PROTECT, null=True, blank=True)
    is_close = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    objects = AcademicSessionManager

    class Meta:
        verbose_name = 'AcademicSession'
        verbose_name_plural = 'AcademicSessions'
        ordering = ['-id']

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('AcademicSession_detail', kwargs={"pk": self.pk})




""" academic calender model """


class AcademicCalender(TimestampAwareModel):
    school = models.ForeignKey(to='schools.School', on_delete=models.PROTECT,null=True, blank=True)
    session_name =models.CharField(max_length=50, null=True, blank=True)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    is_active = models.BooleanField(default=False)
    objects = AcademicCalenderManager

    class Meta:
        verbose_name = 'AcademicCalender'
        verbose_name_plural = 'AcademicCalenders'
        ordering = ['-id']
        

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('AcademicCalender_detail', kwargs={"pk": self.pk})



