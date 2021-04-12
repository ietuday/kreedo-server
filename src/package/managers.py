from django.db import models


""" Package Queryset """


class PackageQueryset(models.QuerySet):
    def name_icontains(self, name):
        return self.filter(name__icontains=name)


""" Package Manager """


class PackageManager(models.Manager):
    def get_queryset(self):
        return PackageQueryset(self.model, using=self._db)

    def name_icontains(self, state):
        return self.get_queryset().name_icontains(name)


""" SchoolPackage Queryset """


class SchoolPackageQueryset(models.QuerySet):
    def is_active(self):
        return self.filter(is_active=True)


""" SchoolPackage Manager """


class SchoolPackageManager(models.Manager):
    def get_queryset(self):
        return SchoolPackageQueryset(self.model, using=self._db)

    def is_active(self, state):
        return self.get_queryset().is_active()
