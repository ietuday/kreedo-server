from django.db import models
from django.urls import reverse
from kreedo.core import TimestampAwareModel
from schools.models import*
from package.managers import *

# Create your models here.


class Package(TimestampAwareModel):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    materials = models.ManyToManyField(to='material.Material', blank=True)
    is_active = models.BooleanField(default=False)
    objects = PackageManager

    class Meta:
        verbose_name = 'Package'
        verbose_name_plural = 'Packages'
        ordering = ['-id']

    def __str__(self):
        return str(self.name)

    def get_absolut_url(self):
        return reverse('Package_details', kwargs={"pk": self.pk})


class SchoolPackage(TimestampAwareModel):
    school = models.ForeignKey(to='schools.School', on_delete=models.PROTECT)
    package = models.ForeignKey('Package', on_delete=models.PROTECT)
    from_date = models.DateField(blank=True)
    to_date = models.DateField(blank=True)
    is_active = models.BooleanField(default=False)
    # custom_materials = models.ManyToManyField(
    #     to='material.Material', blank=True)
    objects = SchoolPackageManager

    class Meta:
        verbose_name = 'SchoolPackage'
        verbose_name_plural = 'SchoolPackages'
        ordering = ['-id']

    def __str__(self):
        return str(self.id)

    def get_absolut_url(self):
        return reverse('SchoolPackage_details', kwargs={"pk": self.pk})
