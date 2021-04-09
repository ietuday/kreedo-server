from django.db import models


""" School  Holiday Queryset """


class SchoolHolidayQueryset(models.QuerySet):
    def is_active(self):
        return self.filter(is_active=True)


""" School  Holiday Manager """


class SchoolHolidayManager(models.Manager):
    def get_queryset(self):
        return SchoolHolidayQueryset(self.model, using=self._db)

    def is_active(self):
        return self.get_queryset().is_active()
