from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView

User = get_user_model()


class UserHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'core/user_home.html'

    # Optional: You can also use the get() method if you need more custom control
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('user_login')  # 'login' should be the name of your login route
        return super().get(request, *args, **kwargs)


class HomeView(TemplateView):
    template_name = 'core/index.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('user_home')
        return super().get(request, *args, **kwargs)
