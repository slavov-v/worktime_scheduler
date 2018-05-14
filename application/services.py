import os
import uuid
from datetime import datetime
from fpdf import FPDF

from django.core.mail import send_mail
from django.core.files.base import ContentFile
from django.contrib.auth import login
from django.http import HttpRequest
from django.utils import timezone

from application.models import User, OvertimeRequest, WorkDay, Report, Ticket, ReportComment


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
    workday_qs = WorkDay.objects.filter(user=user, date=date)
    if not workday_qs.exists():
        return 'You need to add availability for this day first'

    workday = workday_qs.first()

    return OvertimeRequest.objects.create(work_time=workday, employer=employer, user=user)


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


def create_report_comment_service(*, report: Report, content: str):
    return ReportComment.objects.create(report=report, content=content)


def calculate_worker_vacation_service(*, user: User):
    passed_workdays = WorkDay.objects.filter(date__lte=timezone.now().date(),
                                             date__gte=timezone.now().replace(month=1, day=1).date()).count()

    return (passed_workdays / 20) * 1.67


def generate_report_pdf(*, report: Report=None):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(100, 100, report.content)
    filename = f'{uuid.uuid4().hex}.pdf'

    pdf.output(filename, 'F')

    with open(filename, 'rb') as f:
        new_file = ContentFile(f.read(), filename)
        report.document = new_file
        report.save()

    os.remove(filename)

    return report.document.url


def send_email_service(*, subject, sender, to, content):
    send_mail(subject, content, sender, [to], fail_silently=False)
