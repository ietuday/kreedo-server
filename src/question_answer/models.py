from django.db import models
from kreedo.core import TimestampAwareModel

# Create your models here.

class QuestionAnswer(TimestampAwareModel):
    question = models.TextField(null=True,blank=True)
    answer = models.TextField(null=True, blank=True)
    pin = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'QuestionAnswer'
        verbose_name_plural = 'QuestionAnswers'
        ordering = ['-id']
    
    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('QuestionAnswer_detail', kwargs={"pk": self.pk})

        