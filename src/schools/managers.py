from django.db import models


""" School Queryset """
class SchoolQueryset(models.QuerySet):
    def name_icontains(self, name):
        return self.filter(name__icontains=name)

""" School Manager """
class SchoolManager(models.Manager): 
    def get_queryset(self):
        return SchoolQueryset(self.model, using=self._db)

    def name_icontains(self,state):
        return self.get_queryset().name_icontains(name)
    