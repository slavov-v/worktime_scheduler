from django.views.generic import FormView
from django.urls import reverse_lazy

from application.services import login_service
from application.forms import CredentialsForm
from application.models import User


class LoginView(FormView):
    form_class = CredentialsForm
    success_url = reverse_lazy('index.html')
    template_name = 'login.html'

    def form_valid(self, form):
        service_result = login_service(request=self.request, **form.cleaned_data)

        if not isinstance(service_result, User):
            form.add_error(field=None, error='Could not authenticate with the provided credentials')

            return super().form_invalid(form)

        return super().form_valid(form)
