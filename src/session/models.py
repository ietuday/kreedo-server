from django.db import models
from django.urls import reverse
from kreedo.core import TimestampAwareModel
from .managers import*
from schools.models import*
# Create your models here.


class SchoolSession(TimestampAwareModel):
    school = models.ForeignKey(to='schools.School', on_delete= models.PROTECT)
    year = models.DateField(blank=True)
    session_from = models.DateField(blank=True)
    session_till = models.DateField(blank=True)
    is_current_session = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    objects = SchoolSessionManager
    


    class Meta:
        verbose_name = 'SchoolSession'
        verbose_name_plural = 'SchoolSessions'
        ordering = ['-id']
    
    def __str__(self):
        return str(self.id)
    
    def get_absolute_url(self):
        return reverse('SchoolSession_detail', kwargs={"pk":self.pk})

class AcademicSession(TimestampAwareModel):
    name = models.CharField(max_length=50)
    # session = models.ForeignKey('')


