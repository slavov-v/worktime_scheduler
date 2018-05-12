from django.views.generic import ListView
from django.utils import timezone

from application.permissions import IsUserAdminPermission
from application.models import Report


class ListDailyReports(IsUserAdminPermission, ListView):
    model = Report
    template_name = 'report_list.html'

    def get_queryset(self):
        return Report.objects.filter(workday__date=timezone.now())
