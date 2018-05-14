from datetime import datetime

from django.contrib.auth import login
from django.http import HttpRequest
from django.utils import timezone

from application.models import User, OvertimeRequest, WorkDay, Report, Ticket


def login_service(*, email: str, password: str, request: HttpRequest):
    user_qs = User.objects.filter(email=email, is_active=True)

    if user_qs.exists():
        user = user_qs.first()

        if user.check_password(password):
            login(request, user)

            return user

        return 'Could not authenticate with the provided credentials'


def create_user_service(*, email: str, password: str):
    if User.objects.filter(email=email).exists():
        return 'User already exists'

    return User.objects.create_user(email=email, password=password, is_active=True)


def handle_overtime_request_service(overtime_request: OvertimeRequest, status):
    overtime_request.status = status
    overtime_request.save()

    return overtime_request


def create_overtime_request_service(*, date: datetime, employer: User, user: User):
    return OvertimeRequest.objects.create(date=date, employer=employer, user=user)


def update_personal_data_service(*, first_name: str, last_name: str, user: User):
    user.first_name = first_name
    user.last_name = last_name

    return user


def create_report_service(*, user: User, content: str):
    return Report.objects.create(content=content, workday=WorkDay.objects.get(date=timezone.now(), user=user))


def create_ticket_service(*, user: User, content: str):
    return Ticket.objects.create(content=content, user=user)


def add_availability_service(*, user: User, date: datetime):
    if WorkDay.objects.filter(user=user, date=date).exists():
        return 'Availability for this day has already been created'

    return WorkDay.objects.create(date=date, user=user)


def edit_user_work_data_service(*, user: User, position: int, hour_salary: float):
    user.position = position
    user.hour_salary = hour_salary

    user.save()

    return user


def calculate_salary_service(*, user: User):
    workdays = WorkDay.objects.filter(user=user,
                                      date__lte=timezone.now().date(),
                                      date__gte=timezone.now().replace(day=1).date())

    total = 0

    for workday in workdays:
        total += workday.hours_worked.hour * user.hour_salary

    return total


def check_user_work_history_service(*, user):
    workdays = WorkDay.objects.filter(user=user,
                                      date__lte=timezone.now().date(),
                                      date__gte=timezone.now().replace(day=1).date())

    return workdays


def delete_user_service(*, user: User):
    user.is_active = False
    user.save()

    return user
