from django.views.generic import ListView, FormView
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from application.forms import CreateReportForm
from application.permissions import IsUserAdminPermission
from application.models import Report
from application.services import create_report_service


class ListDailyReports(LoginRequiredMixin, IsUserAdminPermission, ListView):
    model = Report
    template_name = 'report_list.html'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        return Report.objects.filter(workday__date=timezone.now())


class CreateReportView(FormView):
    form_class = CreateReportForm
    success_url = reverse_lazy('index')
    template_name = 'create_report.html'
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        create_report_service(user=self.request.user, content=form.cleaned_data.get('content'))

        return super().form_valid(form)
