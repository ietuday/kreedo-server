from django.db import models



""" Child Queryset """


class ChildQueryset(models.QuerySet):
    def first_name_icontains(self, name):
        return self.filter(first_name__icontains=name)

    def last_name_icontains(self, name):
            return self.filter(last_name__icontains=name)


""" Child Manager """


class ChildManager(models.Manager):
    def get_queryset(self):
        return ChildQueryset(self.model, using=self._db)

    def first_name_icontains(self, first_name):
        return self.get_queryset().first_name_icontains(first_name)
    
    def last_name_icontains(self, last_name):
            return self.get_queryset().last_name_icontains(last_name)

