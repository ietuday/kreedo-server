from django.db import models



""" PeriodTemplate Queryset """


class PeriodTemplateQueryset(models.QuerySet):
    def name_icontains(self, name):
        return self.filter(name__icontains=name)


""" PeriodTemplate Manager """


class PeriodTemplateManager(models.Manager):
    def get_queryset(self):
        return PeriodTemplateQueryset(self.model, using=self._db)

    def name_icontains(self, name):
        return self.get_queryset().name_icontains(name)
   