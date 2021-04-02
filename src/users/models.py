from django.db import models
from django.conf import settings
from django.urls import reverse

from django.contrib.auth.models import User

from kreedo.core import TimestampAwareModel
from users.managers import *
from address.models import*
from schools.models import *
# Create your models here.

"""  Relationship Choice """
Mother = 'Mother'
Father = 'Father'
Guardian = 'Guardian'

Relationship_With_Child_Choice = [
        (Mother, 'Mother'),
        (Father, 'Father'),
        (Guardian, 'Guardian')
    ]

""" Role Model """
class Role(TimestampAwareModel):
    name = models.CharField(max_length=50, null=True,blank=True, unique=True)
    is_kreedo = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    web_kreedo = models.BooleanField(default=False)
    web_school_account_owner = models.BooleanField(default=False)
    web_school_school_admin = models.BooleanField(default=False)
    mobile_app_accessor = models.BooleanField(default=False)
    mobile_app_collabrator = models.BooleanField(default=False)
    mobile_app_teacher = models.BooleanField(default=False)
    assigned_to_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    objects  = RoleManager

    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        ordering = ['-id']

    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self):
        return reverse('Role_detail', kwargs={"pk":self.pk})

""" User Detail Model """
class UserDetail(TimestampAwareModel):
    user_obj = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field='id', primary_key=True)
    phone = models.IntegerField(null=True, blank=True)
    activation_key = models.TextField(blank=True, null=False, default='', verbose_name='Activation Key')
    activation_key_expires = models.DateTimeField(blank=True,null=True,
            verbose_name='Activation Key Expiration DateTime')
    address = models.ForeignKey(to='address.Address', on_delete=models.CASCADE, null=True, blank=True)
    reason_for_discontinution = models.TextField(blank=True,null=True)
    relationship_with_child = models.CharField(max_length=25, choices=Relationship_With_Child_Choice)
    role = models.ManyToManyField(Role, related_name='user_role', blank=True)
    own_schools = models.ManyToManyField(School, related_name='user_own_schools', blank=True)
    email_verified = models.BooleanField(default=False,verbose_name='Email Verified')
    phone_verified = models.BooleanField(default=False, verbose_name='Phone Verified')
    school = models.ForeignKey(to='schools.School', on_delete=models.CASCADE, related_name='user_school', null=True, blank=True)

    class Meta:
        verbose_name = 'UserDetail'
        verbose_name_plural = 'UserDetails'
        ordering = ['-user_obj' ]

    def __str__(self):
        return str(self.user_obj)

    def get_absolute_url(self):
        return reverse('UserDetail_detail', kwargs={"pk":self.pk})


class ReportingTo(TimestampAwareModel):
    reporting_to = models.ForeignKey('UserDetail', on_delete=models.CASCADE, null=True, blank=True)
    role = models.ForeignKey('Role', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey('UserDetail', on_delete=models.CASCADE,related_name='user', null=True,blank=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'ReportingTo'
        verbose_name_plural =  'ReportingTos'
    
    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('ReportingTo_detail', kwargs={"pk":self.pk})