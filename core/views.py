from django.http import JsonResponse
from django.http import Http404

from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView
from rest_framework.pagination import CursorPagination
from rest_framework.response import Response
from rest_framework.views import APIView
# from rre.authentication import SessionTokenAuthentication
from rre_test.permission import CustomPermission
# from utils import mongo_utils, ui_utils

# from .models import Client
# from .serializers import ClientSerializer, ClientAutoCompleteSerializer, ClientUpdateSerializer

from core.models import ProfileModel


from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

# from . serializers import CustomerSerializer
from . serializers import UserProfileSerializer, UserSerializer
from django.contrib.auth.models import User

from django.utils import timezone
from datetime import timedelta


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        # token = self.token_expire_handler(token)
        # return Response({'token': token.key})
        return Response(f'Token {token.key}')

    # # this return left time
    # @staticmethod
    # def expires_in(token):
    #     time_elapsed = timezone.now() - token.created
    #     left_time = timedelta(
    #         seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
    #     return left_time

    # # token checker if token expired or not
    # def is_token_expired(self, token):
    #     return self.expires_in(token) < timedelta(seconds=0)

    # # If token is expired new token will be provided
    # # If token is expired then it will be removed and new one with different key will be created
    # def token_expire_handler(self, token):
    #     is_expired = self.is_token_expired(token)
    #     if is_expired:
    #         token.delete()
    #         token = Token.objects.create(user=token.user)
    #     return token


obtain_auth_token = CustomAuthToken.as_view()


class FEView(APIView):
    # authentication_classes = [SessionTokenAuthentication]
    permission_classes = [CustomPermission]

    @staticmethod
    def config(db):
        return mongo_utils.get_system_configuration_with_db(db)


class CheckCanViewPremissionView(FEView):
    # permissions_required = {"GET": 'can_view_permission'}

    def get(self, request):
        content = {'message': 'Hello ! can view permission'}
        return Response(content)


class CheckCanAddPremissionView(FEView):
    # permissions_required = {"GET": 'can_view_permission'}

    def get(self, request):
        content = {'message': 'Hello ! can add permission'}
        return Response(content)


class AssignedUsers:
    def get_users(self, id):
        try:
            if self.request.user.is_superuser:
                usr = User.objects.get(id=id)
            else:
                usr = User.objects.filter(
                    profile__owner_assigned=self.request.user).get(id=id)
            return usr
        except:
            pass
        return


'''user api (user+profile)'''

# View all users


class UserList(FEView):
    permissions_required = {"GET": 'core_profile_read'}

    def get(self, request):
        if self.request.user.is_superuser:
            users = User.objects.all()
        elif self.request.user.profile.is_subadmin():
            users = User.objects.filter(
                profile__owner_assigned=self.request.user)
        elif self.request.user.profile.is_customer():
            users = User.objects.filter(username=self.request.user)

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


# View single user detail
class UserDetail(FEView):
    permissions_required = {"GET": 'core_profile_read'}

    def get(self,  *args, **kwargs):
        # self.request.user.profile.is_subadmin()
        try:

            if self.request.user.is_superuser:
                usr = User.objects.get(id=self.kwargs['id'])
            elif self.request.user.profile.is_subadmin():
                usr = User.objects.filter(
                    profile__owner_assigned=self.request.user).get(id=self.kwargs['id'])
            elif self.request.user.profile.is_customer():
                usr = User.objects.get(id=self.request.user.id)

            # usr = print(AssignedUsers.get_users(self, self.kwargs['id']))
            serializer = UserSerializer(instance=usr)
            return Response(serializer.data)
        except User.DoesNotExist:
            raise Http404


# change single user detail
class UserChange(FEView):
    permissions_required = {"PUT": 'core_profile_update'}

    def put(self, request, *args, **kwargs):
        try:
            if self.request.user.is_superuser:
                usr = User.objects.get(id=self.kwargs['id'])
            elif self.request.user.profile.is_subadmin():
                usr = User.objects.filter(
                    profile__owner_assigned=self.request.user).get(id=self.kwargs['id'])
            elif self.request.user.profile.is_customer():
                usr = User.objects.get(id=self.request.user.id)
            serializer = UserSerializer(usr, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            raise Http404


# Create single user
class UserCreate(FEView):
    permissions_required = {"POST": 'core_profile_create'}

    def post(self, request, format=None):
        if self.request.user.is_superuser | self.request.user.profile.is_subadmin():
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete single User
class UserDelete(FEView):
    permissions_required = {"DELETE": 'core_profile_delete'}

    def delete(self, request, *args, **kwargs):
        try:
            if self.request.user.is_superuser:
                usr = User.objects.get(id=self.kwargs['id'])
            elif self.request.user.profile.is_subadmin():
                usr = User.objects.filter(
                    profile__owner_assigned=self.request.user).get(id=self.kwargs['id'])
            usr.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            raise Http404


# partial Update single User


class UserPatch(FEView):
    permissions_required = {"PATCH": 'core_profile_patch'}

    def patch(self, request, *args, **kwargs):
        print('patch...')
        if self.request.user.is_superuser:
            usr = User.objects.get(id=self.kwargs['id'])
        elif self.request.user.profile.is_subadmin():
            usr = User.objects.filter(
                profile__owner_assigned=self.request.user).get(id=self.kwargs['id'])
        print(usr)
        serializer = UserSerializer(usr, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #     return JsonResponse(code=201, data=serializer.data)
        # return JsonResponse(code=400, data="wrong parameters")


# customer api


# class CustomerList(FEView):
#     permissions_required = {
#         "GET": 'can_view_permission', "POST": 'can_add_permission'}

#     def get(self, request):
#         if self.request.user.is_superuser:
#             custs = User.objects.all()
#         else:
#             custs = User.objects.filter(
#                 profile__owner_assigned=self.request.user)
#         customers = custs
#         serializer = CustomerSerializer(customers, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = CustomerSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CustomerDetail(APIView):
#     permissions_required = {
#         "GET": 'can_view_permission', "PUT": 'can_change_permission', "DELETE": 'can_delete_permission'}

#     def get(self,  *args, **kwargs):
#         try:
#             if self.request.user.is_superuser:
#                 customer = User.objects.get(id=self.kwargs['id'])
#             else:
#                 customer = User.objects.filter(
#                     profile__owner_assigned=self.request.user).get(id=self.kwargs['id'])
#             serializer = CustomerSerializer(instance=customer)
#             return Response(serializer.data)
#         except User.DoesNotExist:
#             raise Http404

#     def put(self, request, *args, **kwargs):
#         try:
#             if self.request.user.is_superuser:
#                 customer = User.objects.get(id=self.kwargs['id'])
#             else:
#                 customer = User.objects.filter(
#                     profile__owner_assigned=self.request.user).get(id=self.kwargs['id'])
#             serializer = CustomerSerializer(customer, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except User.DoesNotExist:
#             raise Http404

#     def delete(self, request, *args, **kwargs):
#         try:
#             if self.request.user.is_superuser:
#                 customer = User.objects.get(id=self.kwargs['id'])
#             else:
#                 customer = User.objects.filter(
#                     profile__owner_assigned=self.request.user).get(id=self.kwargs['id'])
#             customer.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except User.DoesNotExist:
#             raise Http404
