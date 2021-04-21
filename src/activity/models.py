from django.db import models
from django.urls import reverse
from kreedo.core import TimestampAwareModel
from users.models import*
from schools.models import*
from area_of_devlopment.models import*
from .managers import*

# Create your models here.

"""  Choice """
Individual = 'Individual'
Group = 'Group'
Remedial = 'Remedial'


Activity_Type_Choice = [
    (Individual, 'Individual'),
    (Group, 'Group'),
    (Remedial, 'Remedial')
]


"""  Activity Choice """
File = 'File'
Image = 'Image'
Video = 'Video'
Text = 'Text'
Link = 'Link'

Activity_Asset_Choice = [
    (File, 'File'),
    (Image, 'Image'),
    (Video, 'Video'),
    (Text, 'Text'),
    (Link, 'Link')
]


""" Activity Model """


class Activity(TimestampAwareModel):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50, choices=Activity_Type_Choice)
    objective = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    notes = models.CharField(max_length=200, blank=True, null=True)
    subject = models.ManyToManyField(to='schools.Subject', blank=True)
    # skill = models.ManyToManyField(to='area_of_devlopment.Skill', relatedblank=True)
    master_material = models.ManyToManyField(to='material.Material')
    supporting_material = models.ManyToManyField(
        to='material.Material', related_name='activity_supporting_material')
    created_by = models.ForeignKey(
        to='users.UserDetail', on_delete=models.PROTECT)
    duration = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    objects = ActivityManager

    class Meta:
        verbose_name = 'Activity'
        verbose_name_plural = 'Activitys'
        ordering = ['-id']

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('Activity_detail', kwargs={"pk": self.pk})


""" Activity Asset Model """


class ActivityAsset(TimestampAwareModel):
    activity = models.ForeignKey(
        'Activity', on_delete=models.PROTECT, null=True, blank=True)
    type = models.CharField(
        max_length=50, choices=Activity_Asset_Choice)
    activity_data = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'ActivityAsset'
        verbose_name_plural = 'ActivityAssets'
        ordering = ['-id']

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('ActivityAsset_detail', kwargs={"pk": self.pk})


""" Group Activity Missed """


class GroupActivityMissed(TimestampAwareModel):
    child = models.ForeignKey(to='child.Child', on_delete = models.PROTECT)
    period =  models.ForeignKey(to='period.Period', on_delete = models.PROTECT, blank=True, null=True)
    activity = models.ForeignKey(
        to='activity.Activity', on_delete=models.PROTECT)
    is_completed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'GroupActivityMissed'
        verbose_name_plural = 'GroupActivityMisseds'
        ordering = ['-id']

    def __str__(self):
        return str(Self.id)

    def get_absolute_url(self):
        return reverse('GroupActivityMissed_detail', kwargs={"pk": self.pk})
