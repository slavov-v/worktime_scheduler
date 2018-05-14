from django.views.generic import View, FormView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, reverse, render
from django.contrib.auth.mixins import LoginRequiredMixin

from application.permissions import IsUserAdminPermission
from application.services import handle_overtime_request_service, create_overtime_request_service
from application.models import OvertimeRequest
from application.forms import RequestOvertimeForm


class HandleOvertimeRequestView(LoginRequiredMixin, IsUserAdminPermission, View):
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


class RequestOvertimeView(LoginRequiredMixin, FormView):
    form_class = RequestOvertimeForm
    template_name = 'request_overtime.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        create_overtime_request_service(**form.cleaned_data, user=self.request.user)

        return super().form_valid(form)
