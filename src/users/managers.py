from django.db import models

""" Role Queryset """
class RoleQueryset(models.QuerySet):
    def is_kreedo_active(self, state):
        return self.filter(is_kreedo=True)

""" Role Manager """
class RoleManager(models.Manager): 
    def get_queryset(self):
        return RoleQueryset(self.model, using=self._db)

    def is_active(self,state):
        return self.get_queryset().is_active()


""" UserType Queryset """
class UserTypeQueryset(models.QuerySet):
    def is_type_active(self):
        return self.filter(is_active=True)

""" UserType Manager """
class UserTypeManager(models.Manager): 
    def get_queryset(self):
        return UserTypeQueryset(self.model, using=self._db)

    def is_active(self):
        return self.get_queryset().is_type_active() 


""" UserDetail Queryset """
class UserDetailQueryset(models.QuerySet):
    def is_email_verified(self):
        return self.filter(email_verified=True)

""" UserDetail Manager """
class UserDetailManager(models.Manager): 
    def get_queryset(self):
        return UserDetailQueryset(self.model, using=self._db)

    def is_active(self):
        return self.get_queryset().is_email_verified() 



""" ReportingTo Queryset """
class ReportingToQueryset(models.QuerySet):
    def is_active(self):
        return self.filter(is_active=True)

""" ReportingTo Manager """
class ReportingToManager(models.Manager): 
    def get_queryset(self):
        return ReportingToQueryset(self.model, using=self._db)

    def is_active(self):
        return self.get_queryset().is_active()    

""" UserRole Queryset """
class UserRoleQueryset(models.QuerySet):
    def is_active(self):
        return self.filter(is_active=True)

""" UserRole Manager """
class UserRoleManager(models.Manager): 
    def get_queryset(self):
        return UserRoleQueryset(self.model, using=self._db)

    def is_active(self):
        return self.get_queryset().is_active()  


