from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views import View


class Login(View):

    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return HttpResponseRedirect('/admin_dashboard/')
            else:
                return HttpResponseRedirect('/sub_admin_dashboard/')
        else:
            return render(request, 'login.html')

    def post(self, request):
        logout(request)
        username = password = ''
        if request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(
                username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if request.user.is_superuser:
                        return HttpResponseRedirect('/admin_dashboard/')
                    elif request.user.profile.role == 'sub_admin':
                        return HttpResponseRedirect('/sub_admin_dashboard/')
                    else:
                        return HttpResponseRedirect('/customer_dashboard/')
            else:
                return render(request, 'login.html', {'err_msg': 'Invalid credentials'})


class Logout(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/login/')
