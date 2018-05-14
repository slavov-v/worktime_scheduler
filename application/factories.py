import factory
import faker
import datetime
from factory.fuzzy import FuzzyChoice

from django.utils import timezone

from application.models import User, WorkDay, Report, ReportComment, OvertimeRequest, Ticket

fake = faker.Factory.create()


class UserFactory(factory.DjangoModelFactory):
    email = factory.LazyAttribute(lambda n: f'{n}{fake.safe_email()}')
    first_name = factory.LazyAttribute(lambda _: fake.first_name())
    last_name = factory.LazyAttribute(lambda _: fake.last_name())
    is_active = True
    is_superuser = False
    position = FuzzyChoice(choice for choice, _ in User.POSITION_CHOICES)
    hour_salary = factory.LazyAttribute(lambda _: fake.random_number())

    class Meta:
        model = User


class WorkDayFactory(factory.DjangoModelFactory):
    date = timezone.now()
    hours_worked = datetime.time(0, 0)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = WorkDay


class ReportFactory(factory.DjangoModelFactory):
    workday = factory.SubFactory(WorkDayFactory)
    content = factory.LazyAttribute(lambda _: fake.text())

    class Meta:
        model = Report


class ReportCommentFactory(factory.DjangoModelFactory):
    report = factory.SubFactory(ReportFactory)
    content = factory.LazyAttribute(lambda _: fake.text())

    class Meta:
        model = ReportComment


class OvertimeRequestFactory(factory.DjangoModelFactory):
    work_time = factory.SubFactory(WorkDayFactory)
    status = OvertimeRequest.PENDING
    user = factory.SubFactory(UserFactory)
    employer = factory.SubFactory(UserFactory)

    class Meta:
        model = OvertimeRequest


class TicketFactory(factory.DjangoModelFactory):
    content = factory.LazyAttribute(lambda _: fake.text())
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Ticket
