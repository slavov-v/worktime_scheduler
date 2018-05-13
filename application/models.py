from datetime import datetime

from django.db import models
from django.contrib.auth.models import PermissionsMixin, BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    DEVELOPER = 1
    TEAM_LEAD = 2
    PROJECT_MANAGER = 3
    CEO = 4
    CTO = 5

    POSITION_CHOICES = (
        (DEVELOPER, 'Developer'),
        (TEAM_LEAD, 'Team Lead'),
        (PROJECT_MANAGER, 'Project Manager'),
        (CEO, 'CEO'),
        (CTO, 'CTO')
    )

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    position = models.IntegerField(choices=POSITION_CHOICES, default=DEVELOPER)
    hour_salary = models.FloatField(default=0)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name


class WorkDay(models.Model):
    date = models.DateField()
    hours_worked = models.TimeField(default=datetime.min.time())
    user = models.ForeignKey(User, related_name='work_days', on_delete=models.DO_NOTHING)


class Report(models.Model):
    workday = models.OneToOneField(WorkDay, related_name='report', on_delete=models.DO_NOTHING)
    content = models.TextField()


class ReportComment(models.Model):
    content = models.TextField()
    report = models.ForeignKey(Report, related_name='comments', on_delete=models.DO_NOTHING)


class OvertimeRequest(models.Model):
    PENDING = 1
    ACCEPTED = 2
    REJECTED = 3

    OVERTIME_REQUEST_STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected')
    )

    work_time = models.OneToOneField(WorkDay, related_name='overtime_request', on_delete=models.CASCADE)
    status = models.IntegerField(choices=OVERTIME_REQUEST_STATUS_CHOICES)
    user = models.ForeignKey(User, related_name='created_overtime_requests', on_delete=models.CASCADE)
    employer = models.ForeignKey(User, related_name='overtime_requests', on_delete=models.CASCADE)


class Ticket(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, related_name='tickets', on_delete=models.CASCADE)
