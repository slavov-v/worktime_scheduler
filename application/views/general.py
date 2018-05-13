import datetime as dt

from django.views.generic import TemplateView, FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import JsonResponse

from application.services import create_ticket_service, add_availability_service
from application.forms import CreateTicketForm, AddAvailabilityForm
from application.models import WorkDay


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
    login_url = reverse_lazy('login')


class CreateTicketView(LoginRequiredMixin, FormView):
    form_class = CreateTicketForm
    success_url = reverse_lazy('index')
    template_name = 'create_ticket.html'
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        create_ticket_service(user=self.request.user, **form.cleaned_data)

        return super().form_valid(form)


class AddAvailabilityView(LoginRequiredMixin, FormView):
    form_class = AddAvailabilityForm
    success_url = reverse_lazy('index')
    template_name = 'add_availability.html'
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        service_result = add_availability_service(user=self.request.user, **form.cleaned_data)

        if not isinstance(service_result, WorkDay):
            form.add_error(field=None, error=service_result)

            return super().form_invalid(form)

        return super().form_valid(form)


class TrackDailyWorktimeView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        workday_qs = WorkDay.objects.filter(user=request.user, date=timezone.now().date())
        workday = workday_qs.first()

        if request.is_ajax():
            return JsonResponse({'hours_worked': str(workday.hours_worked)})

        return render(request, 'track_worktime.html', {'hours_worked': str(workday.hours_worked)})

    def post(self, request, *args, **kwargs):
        workday_qs = WorkDay.objects.filter(user=request.user, date=timezone.now().date())

        if not workday_qs.exists():
            return JsonResponse({'error': 'No availability added for today'})

        workday = workday_qs.first()
        new_workhours = dt.datetime.combine(dt.datetime(1, 1, 1).date(), workday.hours_worked) + dt.timedelta(seconds=5)
        workday.hours_worked = new_workhours
        workday.save()

        return JsonResponse({'hours_worked': str(new_workhours.time())})
