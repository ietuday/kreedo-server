from django.db import models
from django.urls import reverse
from kreedo.core import TimestampAwareModel
from session.models import*
from .managers import SchoolHolidayManager
from schools.models import*

# Create your models here.

"""  Holiday choice """
Planned_Holiday = 'Planned Holiday'
Unplanned_Holiday = 'Unplanned Holiday'
No_activity_day = 'No activity day'


Holidaye_Type_Choice = [
    (Planned_Holiday, 'Planned Holiday'),
    (Unplanned_Holiday, 'Unplanned Holiday'),
    (No_activity_day, 'No activity day')
]

""" Holiday Type Model """
class HolidayType(TimestampAwareModel):
    holiday_type = models.CharField(max_length = 50)
    color_code = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'HolidayType'
        verbose_name_plural = 'HolidayTypes'
        ordering=['-id']
    
    def __str__(self):
        return str(self.holiday_type)
    
    def get_absolute_url(self):
        return reverse('HolidayType_detail', kwargs={"pk":self.pk})




""" School Holiday Model """


class SchoolHoliday(TimestampAwareModel):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    school_session = models.ForeignKey(to='session.SchoolSession', on_delete=models.PROTECT, null=True,blank=True)
    academic_calender = models.ForeignKey(to='session.AcademicCalender', on_delete = models.PROTECT, null=True,blank=True)
    academic_session = models.ManyToManyField(to='session.AcademicSession', blank=True)
    
    holiday_from = models.DateField(blank=True)
    holiday_till = models.DateField(blank=True)
    # type = models.CharField(
    #     max_length=50, choices=Holidaye_Type_Choice)
    holiday_type = models.ForeignKey('HolidayType',on_delete=models.PROTECT, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    objects = SchoolHolidayManager

    class Meta:
        verbose_name = 'SchoolHoliday'
        verbose_name_plural = 'SchoolHolidays'
        ordering = ['-id']

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('SchoolHoliday', kwargs={"pk": self.pk})


""" School Weak off Model """


class SchoolWeakOff(TimestampAwareModel):
    school = models.ForeignKey(
        to='schools.School', on_delete=models.PROTECT, null=True, blank=True)
    academic_calender = models.ForeignKey(to='session.AcademicCalender', on_delete = models.PROTECT, null=True,blank=True)

    academic_session = models.ForeignKey(
        to='session.AcademicSession', on_delete=models.PROTECT, null=True, blank=True)
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'SchoolWeakOff'
        verbose_name_plural = 'SchoolWeakOffs'
        ordering = ['-id']

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('SchoolWeakOff_detail', kwargs={"pk": self.pk})
