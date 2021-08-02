from django.db import models
from django.urls import reverse
from kreedo.core import TimestampAwareModel
from schools.models import*
from session.models import AcademicSession
from activity.models import*
from .managers import*
from child.models import*

# Create your models here.


""" Plan Sub-Type Relationship Choice """
Sequential = 'Sequential'
Randomized = 'Randomized'


Plan_Sub_Type_Choice = [
    (Sequential, 'Sequential'),
    (Randomized, 'Randomized')
]

"""  Plan Type Relationship Choice """
Individual = 'Individual'
Group = 'Group'


Plan_Type_Choice = [
    (Individual, 'Individual'),
    (Group, 'Group')
]

Yes = 'Yes'
No = 'No'


Previous_Session_Choice = [
    (Yes, 'Yes'),
    (No, 'No')
]


""" Plan Model """


class Plan(TimestampAwareModel):
    name = models.CharField(max_length=100)
    type = models.CharField(
        max_length=50, choices=Plan_Type_Choice, null=True, blank=True)
    sub_type = models.CharField(
        max_length=50,choices=Plan_Sub_Type_Choice, null=True, blank=True)
    is_group = models.BooleanField(default=False)
    grade = models.ForeignKey(to='schools.Grade', on_delete=models.PROTECT)
    subject = models.ForeignKey(to='schools.Subject', on_delete=models.PROTECT,
                                related_name='plan_subject', null=True, blank=True)
    range_from = models.IntegerField(null=True, blank=True)
    range_to = models.IntegerField(null=True, blank=True)
    previous_kreedo = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    objects = PlanManager

    class Meta:
        verbose_name = 'Plan'
        verbose_name_plural = 'Plans'
        ordering = ['-id']

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('Plan_detail', kwargs={"pk": self.pk})


""" Plan Activity Model """


class PlanActivity(TimestampAwareModel):
    plan = models.ForeignKey(
        'Plan', on_delete=models.PROTECT, null=True, blank=True)
    activity = models.ForeignKey(
        to='activity.Activity', on_delete=models.PROTECT, null=True, blank=True)
    sort_no = models.IntegerField(null=True, blank=True)
    is_optional = models.BooleanField(default=False)
    dependent_on = models.ForeignKey(
        to='activity.Activity', on_delete=models.PROTECT, related_name='activity_dependent_on', null=True, blank=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'PlanActivity'
        verbose_name_plural = 'PlanActivitys'
        ordering = ['-id']

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('PlanActivity_detail', kwargs={"pk": self.pk})


""" Subject School Grade Plan Model """


class SubjectSchoolGradePlan(TimestampAwareModel):
    school = models.ForeignKey(to='schools.School', on_delete=models.PROTECT)
    subject = models.ForeignKey(to='schools.Subject', on_delete=models.PROTECT)
    subject_label = models.CharField(max_length=100, blank=True, null=True)
    grade = models.ForeignKey(to='schools.Grade', on_delete=models.PROTECT)
    grade_label = models.CharField(max_length=100, blank=True, null=True)
    plan = models.ForeignKey(
        'Plan', on_delete=models.PROTECT, blank=True, null=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'SubjectSchoolGradePlan'
        verbose_name_plural = 'SubjectSchoolGradePlans'
        ordering = ['-id']

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('SubjectSchoolGradePlan_detail', kwargs={"pk": self.pk})


""" Child Plan Model """


class ChildPlan(TimestampAwareModel):
    name = models.CharField(max_length=100)
    range_of_working_days = models.IntegerField(null=True, blank=True)
    child = models.ForeignKey(
        to='child.Child', on_delete=models.PROTECT, related_name='child_plan', null=True, blank=True)
    subject_school_grade_plan = models.ForeignKey(
        'SubjectSchoolGradePlan', on_delete=models.PROTECT, null=True, blank=True)
    academic_session = models.ForeignKey(
        to='session.AcademicSession', on_delete=models.PROTECT, null=True, blank=True)
    subjects = models.ManyToManyField(to='schools.Subject')
    current_start_date = models.DateField(null=True, blank=True)
    current_end_date = models.DateField(null=True, blank=True)
    class_teacher = models.ForeignKey(
        to='users.UserDetail', on_delete=models.PROTECT, null=True, blank=True)
    kreedo_previous_session = models.CharField(
        max_length=5, default="No")
    curriculum_start_date = models.DateField(null=True, blank=True)

    published = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_close = models.BooleanField(default=False)
    objects = ChildPlanManager

    class Meta:
        verbose_name = 'ChildPlan'
        verbose_name_plural = 'ChildPlans'
        ordering = ['-id']

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('ChildPlan_detail', kwargs={"pk": self.pk})
