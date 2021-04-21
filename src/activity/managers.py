from django.db import models



""" Activity Queryset """


class ActivityQueryset(models.QuerySet):
    def name_icontains(self, name):
        return self.filter(name__icontains=name)


""" Activity Manager """


class ActivityManager(models.Manager):
    def get_queryset(self):
        return ActivityQueryset(self.model, using=self._db)

    def name_icontains(self, name):
        return self.get_queryset().name_icontains(name)




""" Child Plan Queryset """


class ChildPlanQueryset(models.QuerySet):
    def name_icontains(self, name):
        return self.filter(name__icontains=name)


""" Child Plan Manager """


class ChildPlanManager(models.Manager):
    def get_queryset(self):
        return ChildPlanQueryset(self.model, using=self._db)

    def name_icontains(self, name):
        return self.get_queryset().name_icontains(name)
   