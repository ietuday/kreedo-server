from django.db import models
from django.urls import reverse
from kreedo.core import TimestampAwareModel
from activity.models import*

# Create your models here.

"""AreaOfDevlopment Model """


class AreaOfDevlopment(TimestampAwareModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    concept = models.ManyToManyField(
        to='Concept', related_name='aod_concept', blank=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'AreaOfDevlopment'
        verbose_name_plural = 'AreaOfDevlopments'
        ordering = ['-id']
        unique_together = ['name', 'description']

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('AreaOfDevlopment_detail', kwargs={"pk": self.pk})


""" Concept Model """


class Concept(TimestampAwareModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    aod = models.ForeignKey('AreaOfDevlopment', related_name='concept_aod',
                            on_delete=models.PROTECT, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Concept'
        verbose_name_plural = 'Concepts'
        ordering = ['-id']
        unique_together = ['name', 'description', 'aod']

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('Concept_detail', kwargs={"pk": self.pk})


""" Skill Model """


class Skill(TimestampAwareModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    concept = models.ForeignKey('Concept', on_delete=models.PROTECT)
    is_active = models.BooleanField(default=False)
    threshold_percentage = models.IntegerField(null=True, blank=True)
    activity = models.ManyToManyField(
        to='activity.Activity', blank=True)
    remed_activity = models.ManyToManyField(
        to='activity.Activity', related_name='skill_remed_activity')

    class Meta:
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'
        ordering = ['-id']
        unique_together = ['name', 'description', 'concept']


    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('Skill_detail', kwargs={"pk": self.pk})
