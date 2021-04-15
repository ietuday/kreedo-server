from django.db import models


""" School Session Queryset """


class SchoolSessionQueryset(models.QuerySet):
    def is_current_session(self):
        return self.filter(is_active=True)


""" School Session Manager """


class SchoolSessionManager(models.Manager):
    def get_queryset(self):
        return SchoolSessionQueryset(self.model, using=self._db)

    def is_current_session(self):
        return self.get_queryset().is_current_session()


""" Academic  Session Queryset """


class AcademicSessionQueryset(models.QuerySet):
    def is_close(self):
        return self.filter(is_active=True)


""" Academic  Session Manager """


class AcademicSessionManager(models.Manager):
    def get_queryset(self):
        return AcademicSessionQueryset(self.model, using=self._db)

    def is_close(self):
        return self.get_queryset().is_close()
