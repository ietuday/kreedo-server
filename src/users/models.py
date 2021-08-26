from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import User

from kreedo.core import TimestampAwareModel
from users.managers import *
from address.models import*
from schools.models import *


"""  Relationship Choice """
Mother = 'Mother'
Father = 'Father'
Guardian = 'Guardian'

Relationship_With_Child_Choice = [
    (Mother, 'Mother'),
    (Father, 'Father'),
    (Guardian, 'Guardian')
]


"""  Choice """
Male = 'Male'
Female = 'Female'
Other = 'Other'


Gender_Choice = [
    (Male, 'Male'),
    (Female, 'Female'),
    (Other, 'Other')
]


""" Type Model """


class UserType(TimestampAwareModel):
    name = models.CharField(max_length=50, null=True, blank=True)
    sub_type = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    objects = UserTypeManager

    class Meta:
        verbose_name = 'UserType'
        verbose_name_plural = 'UserTypes'
        ordering = ['-id']

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('UserType_detail', kwargs={"pk": self.pk})


""" Role Model """


class Role(TimestampAwareModel):
    name = models.CharField(max_length=50, null=True, blank=True)
    type = models.ForeignKey(UserType, on_delete=models.CASCADE)
    group = models.OneToOneField(
        'auth.Group', on_delete=models.CASCADE, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    objects = RoleManager

    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        ordering = ['-id']
        # unique_together = ['name', 'type', 'is_active']

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('Role_detail', kwargs={"pk": self.pk})


""" User Detail Model """


class UserDetail(TimestampAwareModel):
    user_obj = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field='id', primary_key=True)
    phone = models.CharField(max_length=25, null=True, blank=True)
    activation_key = models.TextField(
        blank=True, null=False, default='', verbose_name='Activation Key')
    activation_key_expires = models.DateTimeField(blank=True, null=True,
                                                  verbose_name='Activation Key Expiration DateTime')
    address = models.ForeignKey(
        to='address.Address', on_delete=models.CASCADE, null=True, blank=True)
    reason_for_discontinution = models.TextField(blank=True, null=True)
    relationship_with_child = models.CharField(
        max_length=25, choices=Relationship_With_Child_Choice, null=True, blank=True)
    type = models.ForeignKey(
        UserType, on_delete=models.PROTECT, null=True, blank=True)
    role = models.ManyToManyField(Role, related_name='user_role', blank=True)
    role_label = models.CharField(max_length=25, null=True, blank=True)
    gender = models.CharField(
        max_length=25, choices=Gender_Choice, null=True, blank=True)
    email_verified = models.BooleanField(
        default=False, verbose_name='Email Verified')
    phone_verified = models.BooleanField(
        default=False, verbose_name='Phone Verified')
    joining_date = models.DateField(null=True)
    photo = models.CharField(max_length=100, null=True, blank=True)
    secret_pin = models.CharField(max_length=50, default='0000')
    is_platform_user = models.BooleanField(default=False)
    objects = UserDetailManager

    class Meta:
        verbose_name = 'UserDetail'
        verbose_name_plural = 'UserDetails'
        ordering = ['-user_obj']

    def __str__(self):
        return str(self.user_obj)

    def get_absolute_url(self):
        return reverse('UserDetail_detail', kwargs={"pk": self.pk})


class ReportingTo(TimestampAwareModel):
    user_detail = models.ForeignKey(
        'UserDetail', on_delete=models.CASCADE, related_name='reporting_to.user_detail+')
    user_role = models.ForeignKey(
        'Role', on_delete=models.CASCADE, related_name='reporting_to.user_role+')
    reporting_to = models.ForeignKey(
        'UserDetail', on_delete=models.SET_NULL, null=True, blank=True)

    is_active = models.BooleanField(default=False)
    objects = ReportingToManager

    class Meta:
        verbose_name = 'ReportingTo'
        verbose_name_plural = 'ReportingTos'

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('ReportingTo_detail', kwargs={"pk": self.pk})


class UserRole(TimestampAwareModel):
    user = models.ForeignKey(
        'UserDetail', on_delete=models.CASCADE, related_name='user')
    role = models.ForeignKey('Role', on_delete=models.CASCADE)
    school = models.ForeignKey(
        to='schools.School', on_delete=models.PROTECT, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    objects = UserRoleManager

    class Meta:
        verbose_name = 'UserRole'
        verbose_name_plural = 'UserRoles'

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('UserRole_detail', kwargs={"pk": self.pk})
