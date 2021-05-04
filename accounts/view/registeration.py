from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from accounts.forms import SignUpForm
from accounts.models import PermissionGroup
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
            # user.profile.role = ''  # sub_admin,, creating user role
            # user.profile.save()
            # permission Group add
            # iusr_group = PermissionGroup.objects.get(name='sub_admin_perm')
            # iusr_group.user_set.add(user)
            print(request.user)
            usr = User.objects.get(username=request.user)
            user.profile.owner_assigned.add(usr)
            user.profile.save()
            messages.success(request, 'Account created successfully')
            return redirect('/signup')
        messages.success(request, 'Validation Error')
        return render(request, 'SignUp.html', {'user_form': user_form})
