from django.db import models
from django.urls import reverse
from kreedo.core import TimestampAwareModel
from schools.models import*
from users.models import*
from activity.models import*
from .managers import*
from session.models import*
from schools.models import*
# Create your models here.


"""  Relationship Choice """
Regular_Assessment_Period = 'Regular Assessment Period'
Regular_Period = 'Regular Period'
Remedial_Period = 'Remedial Period'
Remedial_Assessment = 'Remedial Assessment'

""" Days Choices """
monday = "MONDAY"
tuesday = "TUESDAY"
wednesday = "WEDNESDAY"
thursday = "THURSDAY"
friday = "FRIDAY"
saturday = "SATURDAY"
sunday = "SUNDAY"


Period_Type_Choice = [
    (Regular_Assessment_Period, 'Regular Assessment Period'),
    (Regular_Period, 'Regular Period'),
    (Remedial_Period, 'Remedial Period'),
    (Remedial_Assessment, 'Remedial Assessment')
]

Days_Choice = [
    (monday, 'MONDAY'),
    (tuesday, 'TUESDAY'),
    (wednesday, 'WEDNESDAY'),
    (thursday, 'THURSDAY'),
    (friday, 'FRIDAY'),
    (saturday, 'SATURDAY'),
    (sunday, 'SUNDAY'),
]

""" Period Template model """


class PeriodTemplate(TimestampAwareModel):
    name = models.CharField(max_length=100)
    school = models.ForeignKey(to='schools.School', on_delete=models.PROTECT)
    is_draft = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    objects = PeriodTemplateManager

    class Meta:
        verbose_name = 'PeriodTemplate'
        verbose_name_plural = 'PeriodTemplates'
        ordering = ['-id']

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('PeriodTemplate_detail', kwargs={"pk": self.pk})


""" Period Model """


class Period(TimestampAwareModel):
    period_template_detail = models.ForeignKey(to='PeriodTemplateDetail',on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=100, blank=True)
    subject = models.ForeignKey(to='schools.Subject', on_delete=models.PROTECT,
                                related_name='period_subject', null=True, blank=True)
    room_no = models.ForeignKey(
        to='schools.Room', on_delete=models.PROTECT, related_name='period_room_no', null=True, blank=True)
    academic_session = models.ManyToManyField(
        to='session.AcademicSession', blank=True)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    type = models.CharField(
        max_length=50, choices=Period_Type_Choice, blank=True)
    teacher = models.ManyToManyField(to='users.UserDetail', blank=True)
    activity_done = models.ManyToManyField(to='activity.Activity', blank=True)
    is_complete = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Period'
        verbose_name_plural = 'Periods'
        ordering = ['-id']
        # unique_together = ('start_time', 'end_time','room_no')

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('Period_detail', kwargs={"pk": self.pk})


""" Period Template Detail """


class PeriodTemplateDetail(TimestampAwareModel):
    period_template = models.ForeignKey(
        'PeriodTemplate', on_delete=models.PROTECT, null=True, blank=True)
    name =  models.CharField(
        max_length=50,null=True,blank=True)
    subject = models.ForeignKey(
        to='schools.Subject', on_delete=models.PROTECT, null=True, blank=True)
    room = models.ForeignKey(
        to='schools.Room', on_delete=models.PROTECT, null=True, blank=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    type = models.CharField(
        max_length=50, choices=Period_Type_Choice)
    days = models.CharField(
        max_length=50, choices=Days_Choice)
    academic_session = models.ForeignKey(
        to='session.AcademicSession', on_delete=models.PROTECT, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'PeriodTemplateDetail'
        verbose_name_plural = 'PeriodTemplateDetails'
        ordering = ['-id']
        unique_together = ('room','start_time','end_time')

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('PeriodTemplateDetail_detail', kwargs={"pk": self.pk})


""" Apply period template to section  and grade """


class PeriodTemplateToGrade(TimestampAwareModel):
    academic_session = models.ForeignKey(
        to='session.AcademicSession', on_delete=models.PROTECT, null=True, blank=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    period_template = models.ForeignKey(
        'PeriodTemplate', on_delete=models.PROTECT, null=True, blank=True)
    is_applied = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'PeriodTemplateToGrade'
        verbose_name_plural = 'PeriodTemplateToGrades'
        ordering = ['-id']

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('PeriodTemplateToGrade_detail', kwargs={"pk": self.pk})
