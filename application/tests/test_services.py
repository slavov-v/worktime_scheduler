import faker
import datetime
from test_plus import TestCase
from unittest import mock

from django.utils import timezone

from application.services import (
    handle_overtime_request_service,
    create_overtime_request_service,
    update_personal_data_service,
    create_report_service,
    create_ticket_service,
    add_availability_service,
    edit_user_work_data_service,
    calculate_salary_service,
    calculate_worker_vacation_service,
    check_user_work_history_service,
    create_report_comment_service,
    generate_report_pdf,
    send_email_service
)
from application.factories import OvertimeRequestFactory, UserFactory, WorkDayFactory, ReportFactory
from application.models import OvertimeRequest, Report, Ticket, WorkDay, User, ReportComment

fake = faker.Factory.create()


class TestHandleOvertimeRequestService(TestCase):
    def test_service_sets_status_successfully(self):
        request = OvertimeRequestFactory()
        self.assertEqual(request.status, OvertimeRequest.PENDING)

        handle_overtime_request_service(overtime_request=request, status=OvertimeRequest.ACCEPTED)
        request.refresh_from_db()
        self.assertEqual(request.status, OvertimeRequest.ACCEPTED)


class TestCreateOvertimeRequestService(TestCase):
    def test_service_creates_instance_successfully(self):
        workday = WorkDayFactory(date=timezone.now().date())
        current_request_count = OvertimeRequest.objects.count()

        create_overtime_request_service(date=workday.date,
                                        user=workday.user,
                                        employer=UserFactory(is_superuser=True))

        self.assertEqual(OvertimeRequest.objects.count(), current_request_count + 1)

    def test_service_returns_error_msg_if_workday_does_not_exist(self):
        service_result = create_overtime_request_service(date=timezone.now().date(),
                                                         user=UserFactory(),
                                                         employer=UserFactory())

        self.assertEqual(service_result, 'You need to add availability for this day first')


class TestUpdatePersonalDataService(TestCase):
    def test_service_updates_data(self):
        user = UserFactory()

        new_fname = fake.first_name()
        new_lname = fake.last_name()

        user = update_personal_data_service(first_name=new_fname,
                                            last_name=new_lname,
                                            user=user)

        self.assertEqual(user.first_name, new_fname)
        self.assertEqual(user.last_name, new_lname)


class TestCreateReportService(TestCase):
    def test_service_creates_instance_successfully(self):
        current_report_count = Report.objects.count()
        workday = WorkDayFactory(date=timezone.now().date())

        create_report_service(user=workday.user, content=fake.text())

        self.assertEqual(Report.objects.count(), current_report_count + 1)


class TestCreateTicketService(TestCase):
    def test_service_creates_instance_successfully(self):
        user = UserFactory()
        current_ticket_count = Ticket.objects.count()
        create_ticket_service(user=user, content=fake.text())

        self.assertEqual(Ticket.objects.count(), current_ticket_count + 1)


class TestAddAvailavilityService(TestCase):
    def test_service_returns_error_msg_if_workday_exists(self):
        workday = WorkDayFactory()

        service_result = add_availability_service(user=workday.user, date=workday.date)

        self.assertEqual(service_result, 'Availability for this day has already been created')

    def test_service_creates_instance_successfully_if_workday_does_not_exist(self):
        current_workday_count = WorkDay.objects.count()
        user = UserFactory()
        add_availability_service(user=user, date=timezone.now().date())

        self.assertEqual(WorkDay.objects.count(), current_workday_count+1)


class TestEditUserWorkDataService(TestCase):
    def test_service_updates_data(self):
        user = UserFactory()
        new_position = User.CTO
        new_salary = fake.random_number()

        edit_user_work_data_service(user=user, position=new_position, hour_salary=new_salary)
        user.refresh_from_db()

        self.assertEqual(user.position, new_position)
        self.assertEqual(user.hour_salary, new_salary)


class TestCalculateSalaryService(TestCase):
    def test_service_calculates_correctly(self):
        user = UserFactory()

        day_count = 0
        for i in range(1, timezone.now().date().day):
            WorkDayFactory(user=user, hours_worked=datetime.time(4, 0))
            day_count += 1

        expected = day_count * 4 * user.hour_salary
        service_result = calculate_salary_service(user=user)

        self.assertEqual(expected, service_result)


class TestCheckUserWorkHistoryService(TestCase):
    def test_service_returns_correct_workdays(self):
        user = UserFactory()

        day_count = 0
        for i in range(1, timezone.now().date().day):
            WorkDayFactory(user=user, hours_worked=datetime.time(4, 0))
            day_count += 1

        service_result = check_user_work_history_service(user=user)

        self.assertEqual(day_count, service_result.count())


class TestCreateReportCommentService(TestCase):
    def test_service_creates_instance_successfully(self):
        report = ReportFactory()
        current_report_comment_count = ReportComment.objects.count()

        create_report_comment_service(report=report, content=fake.text())

        self.assertEqual(ReportComment.objects.count(), current_report_comment_count+1)


class TestCalculateWorkerVacationService(TestCase):
    def test_service_calculates_vacation_days_correctly(self):
        days_worked = 0
        user = UserFactory()

        for i in range(1, timezone.now().date().month):
            for j in range(1, timezone.now().date().day):
                WorkDayFactory(user=user)
                days_worked += 1

        expected = (days_worked/20) * 1.67
        service_result = calculate_worker_vacation_service(user=user)

        self.assertEqual(service_result, expected)


class TestGenerateReportPDFService(TestCase):
    def test_service_creates_document_for_report(self):
        report = ReportFactory()

        generate_report_pdf(report=report)
        report.refresh_from_db()

        self.assertIsNotNone(report.document.path)


@mock.patch('application.services.send_mail')
class TestSendEmailService(TestCase):
    def test_service_calls_send_mail_correctly(self, send_email_mock):
        subject = fake.word()
        sender = fake.safe_email()
        to = fake.safe_email(),
        content = fake.text()
        send_email_service(subject=subject,
                           sender=sender,
                           to=to,
                           content=content)

        self.assertTrue(send_email_mock.called)
        send_email_mock.assert_called_with(subject, content, sender, [to], fail_silently=False)
