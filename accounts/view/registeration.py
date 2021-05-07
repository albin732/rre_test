from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from accounts.forms import SignUpForm
from accounts.models import PermissionGroup, Role
from core.models import Profile
# from django.contrib.auth.models import Group
from django.contrib.auth.models import User


class SignUp(View):

    def get(self, request):
        user_form = SignUpForm()
        return render(request, 'SignUp.html', {'user_form': user_form})

    def post(self, request):
        user_form = SignUpForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            # usr = User.objects.get(username=request.user)
            # user.profile.owner_assigned.add(usr)
            user.profile.role = Role.objects.get(name='client')
            user.profile.save()
            messages.success(request, 'Account created successfully')
            return redirect('/signup')
        messages.success(request, 'Validation Error')
        return render(request, 'SignUp.html', {'user_form': user_form})
