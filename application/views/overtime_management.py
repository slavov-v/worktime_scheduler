from django.views.generic import View, ListView
from django.shortcuts import get_object_or_404, redirect, reverse, render
from django.utils import timezone

from application.permissions import IsUserAdminPermission
from application.services import handle_overtime_request_service
from application.models import OvertimeRequest, Report


class HandleOvertimeRequestView(IsUserAdminPermission, View):
    def post(self, request, *args, **kwargs):
        overtime_request = get_object_or_404(OvertimeRequest,
                                             id=request.POST.get('ot_request_id'),
                                             employer_id=request.user.id)

        handle_overtime_request_service(overtime_request, int(status=request.POST.get('status')))

        return redirect(reverse('index'))

    def get(self, request, *args, **kwargs):
        context = {
            'overtime_requests': OvertimeRequest.objects.filter(employer_id=request.user.id,
                                                                status=OvertimeRequest.PENDING)
        }

        return render(request, 'overtime_requests_list.html', context)
