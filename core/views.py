from django.http import Http404

from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.pagination import CursorPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rre.authentication import SessionTokenAuthentication
from rre.permission import CustomPermission
from utils import mongo_utils, ui_utils

from .models import Client
from .serializers import ClientSerializer, ClientAutoCompleteSerializer, ClientUpdateSerializer


class FEView(APIView):
    authentication_classes = [SessionTokenAuthentication]
    permission_classes = [CustomPermission]
    @staticmethod
    def config(db):
        return mongo_utils.get_system_configuration_with_db(db)


class CustomPagination(CursorPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000
    ordering = '-id'


class Logout(FEView):
    def post(self, request):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)


class ClientAutoComplete(FEView):

    permissions_required = {"GET": 'CLIENT_AUTOCOMPLETE'}

    def get(self, request, client=None):
        if client:
            clients = Client.objects.filter(name__startswith=client)[:10]
        else:
            clients = Client.objects.all()[:10]
        clients = ClientAutoCompleteSerializer(clients, many=True)
        return Response(data={'results': clients.data})


class AccountAutoComplete(FEView):

    permissions_required = {"GET": 'ACCOUNT_AUTOCOMPLETE'}

    def get(self, request):
        db = request.mongodb
        account = request.query_params.get('q', '')
        if account:
            key = "^" + account
            accounts = db['accounts'].find({"id_": {"$regex": key}}).limit(15)
        result = [{'id': i['id_'], 'name': i['id_']} for i in accounts]
        return Response(data={'results': result})


class ClientsView(ListAPIView, FEView):

    permissions_required = {"GET": 'CLIENTS_LIST_VIEW'}

    pagination_class = CustomPagination
    queryset = Client.objects.select_related('user').filter(is_active=True)
    serializer_class = ClientSerializer


class ClientAddView(CreateAPIView, FEView):

    permissions_required = {"POST": 'CLIENT_ADD'}
    print('client Add View')
    # serializer_class = ClientSerializer


class ClientEditView(UpdateAPIView, FEView):

    permissions_required = {"PUT": 'CLIENT_EDIT'}

    queryset = Client.objects.all()
    serializer_class = ClientUpdateSerializer


class ClientDeleteView(FEView):

    permissions_required = {"DELETE": 'CLIENT_DELETE'}

    def delete(self, request, pk, format=None):
        try:
            client = Client.objects.filter(is_active=True).get(pk=pk)
        except Client.DoesNotExist:
            raise Http404
        client.is_active = False
        user_ = client.user
        user_.is_active = False
        client.save()
        user_.save()
        return Response({"detail": "Deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class SystemSettings(FEView):

    permissions_required = {"POST": 'SYS_SETTINGS_ADD'}

    def post(self, request):
        thresholds = ui_utils.build_system_settings(self.config(request.mongodb))
        return Response({'thresholds': thresholds})


class SystemSettingsUpdate(FEView):

    permissions_required = {"POST": 'SYS_SETTINGS_UPDATE'}

    def post(self, request):
        thresholds = ui_utils.build_new_system_settings(self.config(request.mongodb), request.data['thresholds'])
        return Response({'thresholds': thresholds})


class RulesConfig(FEView):

    permissions_required = {"POST": 'RULES_CONFIG_ADD'}

    def post(self, request):
        rules = ui_utils.build_rules_from_config(self.config(request.mongodb))
        return Response({'rules': rules})


class RulesUpdate(FEView):

    permissions_required = {"POST": 'RULES_CONFIG_UPDATE'}

    def post(self, request):
        rules = ui_utils.build_new_rules(self.config(request.mongodb), request.data['rules'])
        return Response({'rules': rules})
