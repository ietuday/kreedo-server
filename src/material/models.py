from django.db import models
from django.urls import reverse
from kreedo.core import TimestampAwareModel
from activity.models import*
# Create your models here.
""" Material Model """


class Material(TimestampAwareModel):
    name = models.CharField(max_length=100)
    decription = models.TextField(null=True, blank=True)
    photo = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materials'
        ordering = ['-id']

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('Material_detail', kwargs={"pk": self.pk})


""" Activity Master Supporting Material Model """


class ActivityMasterSupportingMaterial(TimestampAwareModel):
    activity = models.ForeignKey(
        to='activity.Activity', on_delete=models.PROTECT)
    master_material = models.ManyToManyField('Material', blank=True)
    supporting_material = models.ManyToManyField(
        'Material', related_name='supporting_material', blank=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'ActivityMasterSupportingMaterial'
        verbose_name_plural = 'ActivityMasterSupportingMaterials'

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('ActivityMasterSupportingMaterial_detail', kwargs={"pk": self.pk})
