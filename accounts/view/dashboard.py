from django.views import View
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator
from common.auth_decorator import role_required
from django.contrib.auth.models import User

admin_decorators = [login_required(
    login_url='/accounts/login/'), role_required('master_admin')]
sub_admin_decorators = [login_required(
    login_url='/accounts/login/'), role_required('sub_admin')]
customer_decorators = [login_required(
    login_url='/accounts/login/')]


# @ method_decorator(admin_decorators, name="dispatch")
# class AdminDashboard(View):
#     def get(self, request):
#         return render(request, "admin_dashboard.html")

# @ method_decorator(sub_admin_decorators, name="dispatch")
# class SubAdminDashboard(View):
#     # @login_required(login_url='/accounts/login/')
#     def get(self, request):
#         return render(request, "sub_admin_dashboard.html")

@ method_decorator(admin_decorators, name="dispatch")
class AdminDashboard(ListView):
    model = User
    template_name = 'admin_dashboard.html'
    context_object_name = 'customers'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        else:
            return User.objects.filter(profile__owner_assigned=self.request.user)


@ method_decorator(sub_admin_decorators, name="dispatch")
class SubAdminDashboard(ListView):
    model = User
    template_name = 'sub_admin_dashboard.html'
    context_object_name = 'customers'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        else:
            return User.objects.filter(profile__owner_assigned=self.request.user)


@ method_decorator(customer_decorators, name="dispatch")
class CustomerDashboard(ListView):
    model = User
    template_name = 'customer_dashboard.html'
    context_object_name = 'customers'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        else:
            return User.objects.filter(profile__owner_assigned=self.request.user)
