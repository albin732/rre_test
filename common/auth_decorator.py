from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied

from django.contrib.auth.decorators import user_passes_test
from core.models import ProfileModel
from django.contrib.auth.models import User
from accounts.models import Role


# roles
def role_required(allowed_roles=[]):
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            if str(request.user.profile.role) in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                raise PermissionDenied
        return wrap
    return decorator


# # groups
# def group_required(*group_names):
#     def in_groups(u):
#         perm = False
#         for g in group_names:
#             if bool(u.groups.filter(name=g)):
#                 perm = True
#                 break
#         if u.is_authenticated:
#             if perm | u.is_superuser:
#                 return True
#         return False
#     return user_passes_test(in_groups)


# # roles
# def role_required(allowed_roles=[]):
#     def decorator(view_func):
#         def wrap(request, *args, **kwargs):
#             print(request.user.profile.role)
#             if request.user.profile.role in allowed_roles:
#                 return view_func(request, *args, **kwargs)
#             else:
#                 raise PermissionDenied
#         return wrap
#     return decorator


# def admin(view_func):
#     def wrap(request, *args, **kwargs):
#         if str(request.user.profile.role) == 'admin':
#             return view_func(request, *args, **kwargs)
#         else:
#             raise PermissionDenied
#     return wrap


# def sub_admin(view_func):
#     def wrap(request, *args, **kwargs):
#         allowed_roles = ['admin', 'sub_admin']
#         if request.user.profile.role in allowed_roles:
#             return view_func(request, *args, **kwargs)
#         else:
#             raise PermissionDenied
#     return wrap
