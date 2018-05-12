from django.contrib.auth.mixins import UserPassesTestMixin


class BaseUserPassesTestMixin(UserPassesTestMixin):
    def test_func(self):
        return True
