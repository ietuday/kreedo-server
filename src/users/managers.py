from django.db import models

""" Role Queryset """
class RoleQueryset(models.QuerySet):
    def is_kreedo_active(self, state):
        return self.filter(is_kreedo=True)

""" Role Manager """
class RoleManager(models.Manager): 
    def get_queryset(self):
        return RoleQueryset(self.model, using=self._db)

    def is_kreedo_active(self,state):
        return self.get_queryset().is_kreedo_active()
    