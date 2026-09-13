from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Only allow authenticated staff users (same rule as Django admin)."""
    login_url = "/control/login/"

    def test_func(self):
        u = self.request.user
        return u.is_authenticated and u.is_staff and u.is_active