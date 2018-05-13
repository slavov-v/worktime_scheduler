from django.views.generic import FormView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect

from application.services import login_service, create_user_service, update_personal_data_service
from application.forms import CredentialsForm, EditPersonalDataForm
from application.models import User
from application.permissions import IsUserAdminPermission


class LoginView(FormView):
    form_class = CredentialsForm
    success_url = reverse_lazy('index')
    template_name = 'login.html'

    def form_valid(self, form):
        service_result = login_service(request=self.request, **form.cleaned_data)

        if not isinstance(service_result, User):
            form.add_error(field=None, error=service_result)

            return super().form_invalid(form)

        return super().form_valid(form)


class LogOutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)

        return redirect(reverse('index'))


class CreateUserView(LoginRequiredMixin, IsUserAdminPermission, FormView):
    form_class = CredentialsForm
    success_url = reverse_lazy('index')
    login_url = reverse_lazy('login')
    template_name = 'create_user.html'

    def form_valid(self, form):
        service_result = create_user_service(**form.cleaned_data)

        if not isinstance(service_result, User):
            form.add_error(field=None, error=service_result)

            return super().form_invalid(form)

        return super().form_valid(form)


class EditPersonalDataView(LoginRequiredMixin, FormView):
    form_class = EditPersonalDataForm
    success_url = reverse_lazy('index')
    template_name = 'edit_personal_data.html'
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        update_personal_data_service(**form.cleaned_data, user=self.request.user)

        return super().form_valid(form)
