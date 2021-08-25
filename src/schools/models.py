from django.db import models
from django.urls import reverse
from kreedo.core import TimestampAwareModel
from schools.managers import*
from users.models import*
from address.models import*
from plan.models import ChildPlan
from session.models import *
from activity.models import*
# Create your models here.

"""  Relationship Choice """
Individual = 'Individual'
Group = 'Group'


Subject_Type_Choice = [
    (Individual, 'Individual'),
    (Group, 'Group')
]


"""  Relationship Choice """
Preschool = 'Preschool'
APS = 'APS'
K12 = 'K12'
HLS = 'HLS'

School_Type_Choice = [
    (Preschool, 'Preschool'),
    (APS, 'APS'),
    (K12, 'K12'),
    (HLS, 'HLS')
]

""" Grade model """


class Grade(TimestampAwareModel):
    name = models.CharField(max_length=50, unique=True)
    school = models.ForeignKey('School', on_delete=models.PROTECT, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Grade'
        verbose_name_plural = 'Grades'
        ordering = ['-id']

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('Grade_detail', kwargs={"pk": self.pk})


class Section(TimestampAwareModel):
    grade = models.ForeignKey(
        'Grade', on_delete=models.PROTECT, null=True, blank=True)
    school = models.ForeignKey('School', on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'
        ordering = ['-id']

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('Section_detail', kwargs={"pk": self.pk})



class Subject(TimestampAwareModel):
    name = models.CharField(max_length=50, null=True, blank=True, unique=True)
    type = models.CharField(
        max_length=50, choices=Subject_Type_Choice, null=True, blank=True)
    activity = models.ManyToManyField(
        to='activity.Activity', related_name='subject_activity', blank=True)
    is_active = models.BooleanField(default=False)
    plan = models.ManyToManyField(ChildPlan, blank=True)
    is_kreedo = models.BooleanField(default=False)
    school = models.ForeignKey("School",on_delete=models.PROTECT,null=True,blank=True)

    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'
        ordering = ['-id']

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('Subject_detail', kwargs={"pk": self.pk})


""" License Model """


class License(TimestampAwareModel):
    total_no_of_user = models.IntegerField()
    total_no_of_children = models.IntegerField()
    licence_from = models.DateField(null=True, blank=True)
    licence_from_time = models.TimeField(null=True, blank=True)
    licence_till = models.DateField(null=True, blank=True)
    licence_till_time = models.TimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        to='users.UserDetail', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'License'
        verbose_name_plural = 'Licenses'
        ordering = ['-id']

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('License_detail', kwargs={'pk': self.pk})


"""School Model"""
class School(TimestampAwareModel):
    name = models.CharField(max_length=50)
    type = models.CharField(
        max_length=50, choices=School_Type_Choice, null=True, blank=True)
    logo = models.URLField(null=True, blank=True)
    address = models.ForeignKey(
        to='address.Address', on_delete=models.CASCADE, null=True, blank=True)
    license = models.ForeignKey(
        'License', on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    account_manager = models.ForeignKey(
        to='users.UserDetail', on_delete=models.PROTECT,null=True, blank=True)
    objects = SchoolManager

    class Meta:
        verbose_name = 'School'
        verbose_name_plural = 'Schools'
        ordering = ['-id']

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('School_detail', kwargs={"pk": self.pk})


""" Section Subject Teacher Model """
 

class SectionSubjectTeacher(TimestampAwareModel):
    subject = models.ForeignKey('Subject', on_delete=models.PROTECT)
    teacher = models.ForeignKey(
        to='users.UserDetail', on_delete=models.PROTECT, null=True, blank=True)
    academic_session = models.ForeignKey(
        to='session.AcademicSession', on_delete=models.PROTECT)
    period = models.ForeignKey(
        to='period.Period', on_delete=models.PROTECT,  null=True, blank=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'SectionSubjectTeacher'
        verbose_name_plural = 'SectionSubjectTeachers'
        ordering = ['-id']

    def __str__(self):
        return str(self.id)

    def get_absolute_url(Self):
        return reverse('SectionSubjectTeacher_detail', kwargs == {"pk": self.pk})


""" Room Model """


class Room(TimestampAwareModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    room_no = models.IntegerField()
    school = models.ForeignKey('School', on_delete=models.PROTECT)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'
        ordering = ['-id']

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('Room_detail', kwargs={"pk": self.pk})


class SchoolGradeSubject(TimestampAwareModel):
    school = models.ForeignKey('School', on_delete=models.PROTECT)
    grade = models.ForeignKey('Grade', on_delete=models.PROTECT)
    subject = models.ManyToManyField(
        'Subject', related_name='school_grade_subject')
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'SchoolGradeSubject'
        verbose_name_plural = 'SchoolGradeSubjects'
        ordering = ['-id']

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('SchoolGradeSubject_detail', kwargs={"pk": self.pk})
