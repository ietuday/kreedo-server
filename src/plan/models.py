from django.db import models
from django.urls import reverse
from kreedo.core import TimestampAwareModel
from schools.models import*
# Create your models here.


class ChildPlan(TimestampAwareModel):
    pass


class SubjectSchoolGradePlan(TimestampAwareModel):
    school = models.ForeignKey(to='schools.School', on_delete=models.PROTECT)
    subject = models.ForeignKey(to='schools.Subject', on_delete=models.PROTECT)
    subject_label = models.CharField(max_length=100, blank=True, null=True)
    grade = models.ForeignKey(to='schools.Grade', on_delete=models.PROTECT)
    grade_label = models.CharField(max_length=100, blank=True, null=True)
    # plan = models.ForeignKey('Plan', on_delete=models.PROTECT)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'SubjectSchoolGradePlan'
        verbose_name_plural = 'SubjectSchoolGradePlans'
        ordering = ['-id']

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('SubjectSchoolGradePlan_detail', kwargs={"pk": self.pk})
