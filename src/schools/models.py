from django.db import models
from django.urls import reverse
from kreedo.core import TimestampAwareModel
from schools.managers import*
from users.models import*
from address.models import*
# Create your models here.

""" School Type Model """
class SchoolType(TimestampAwareModel):
    name = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'SchoolType'
        verbose_name_plural = 'SchoolTypes'
        ordering = ['-id']

    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self):
        return reverse('SchoolType_detail', kwargs={"pk":self.pk})


""" School License Model"""
class SchoolLicense(TimestampAwareModel):
    total_user = models.IntegerField(null=True, blank=True)
    total_children = models.IntegerField(null=True, blank=True)
    license_from = models.DateTimeField(blank=True,null=True)
    license_till = models.DateTimeField(blank=True,null=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    created_by = models.ForeignKey(to='users.UserDetail', on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'SchoolLicense'
        verbose_name_plural = 'SchoolLicenses'
    
    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('SchoolLicense_detail', kwargs={"pk":self.pk})


"""School Model"""
class School(TimestampAwareModel):
    name = models.CharField(max_length=50, null=True, blank=True)
    school_type  = models.ForeignKey('SchoolType', on_delete=models.CASCADE, null=True, blank=True)
    logo = models.URLField(null=True, blank=True)
    address = models.ForeignKey(to='address.Address', on_delete=models.CASCADE, null=True,blank=True)
    license = models.ForeignKey('SchoolLicense', on_delete=models.CASCADE, null=True, blank=True)
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


        
    