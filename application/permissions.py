from django.contrib.auth.mixins import UserPassesTestMixin


class BaseUserPassesTestMixin(UserPassesTestMixin):
    def test_func(self):
        return True


class IsUserAdminPermission(BaseUserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_superuser:
            return True and super().test_func()

        return False
