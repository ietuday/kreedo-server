from django.db import models
from django.urls import reverse
from kreedo.core import TimestampAwareModel
from schools.managers import*
from users.models import*
from address.models import*
from plan.models import ChildPlan
# Create your models here.


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
    name = models.CharField(max_length=50,unique=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Grade'
        verbose_name_plural = 'Grades'
        ordering = ['-id']

    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self):
        return reverse('Grade_detail',kwargs={"pk":self.pk})

class Section(TimestampAwareModel):
    name = models.CharField(max_length=50,unique=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'
        ordering = ['-id']

    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self):
        return reverse('Section_detail',kwargs={"pk":self.pk})

class Subject(TimestampAwareModel):
    name = models.CharField(max_length=50, unique=True)
    is_active =models.BooleanField(default=False)
    plan = models.ManyToManyField(ChildPlan, blank=True)
    is_kreedo = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'
        ordering = ['-id']

    def __str__(self):
        return reverse('Subject_detail',kwargs={"pk":self.pk})

    def get_absolute_url(self):
        return reverse('Subject_detail',kwargs={"pk":self.pk})



""" License Model """
class License(TimestampAwareModel):
    total_no_of_user = models.IntegerField()
    total_no_of_children = models.IntegerField()
    licence_from = models.DateTimeField(blank=True)
    licence_till = models.DateTimeField(blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.ForeignKey(to= 'users.UserDetail',on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'License'
        verbose_name_plural = 'Licenses'
        ordering = ['-id']
    
    def __str__(self):
        return str(self.id)
    
    def get_absolute_url(self):
        return reverse('License_detail',kwargs={'pk':self.pk})



    
"""School Model"""
class School(TimestampAwareModel):
    name = models.CharField(max_length=50, null=True, blank=True)
    type = models.CharField(max_length=50,choices = School_Type_Choice, null=True, blank=True)
    logo = models.URLField(null=True, blank=True)
    address = models.ForeignKey(to='address.Address', on_delete=models.CASCADE, null=True,blank=True)
    license = models.ForeignKey('License', on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    objects = SchoolManager

    class Meta:
        verbose_name = 'School'
        verbose_name_plural = 'Schools'
        ordering = ['-id']
        
    
    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self):
        return reverse('School_detail', kwargs = {"pk":self.pk})




        
    