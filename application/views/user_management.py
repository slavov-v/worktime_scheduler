from django.views.generic import FormView
from django.urls import reverse_lazy

from application.services import login_service, create_user_service
from application.forms import CredentialsForm
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


class CreateUserView(IsUserAdminPermission, FormView):
    form_class = CredentialsForm
    success_url = reverse_lazy('index')
    template_name = 'create_user.html'

    def form_valid(self, form):
        service_result = create_user_service(**form.cleaned_data)

        if not isinstance(service_result, User):
            form.add_error(field=None, error=service_result)

            return super().form_invalid(form)

        return super().form_valid(form)
