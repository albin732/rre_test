import logging
from re import sub

from django.http import JsonResponse

from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin

from rest_framework.authtoken.models import Token

# from utils.mongo_utils import initialize_mongo_instance
# from core.models import ClientConfig


class MongoDBSelectorMiddleware(MiddlewareMixin):

    def process_request(self, request):
        header_token = request.META.get('HTTP_AUTHORIZATION', None)
        # header_token = 'b436c73f2cef4faaab0172f6943869ca89cfff38' q
        # a1@a.com bd1d969b932db8ad3760baf57661b33ac62af155
        if header_token is not None:
            try:
                token = sub('Token ', '', request.META.get(
                    'HTTP_AUTHORIZATION', None))
                token_obj = Token.objects.get(key=token)
                user = token_obj.user
                request.user = user
                perm_group = request.user.profile.all_permissions()
                request.permissions = [
                    i.name for i in perm_group] if user.profile.role else []

            except Token.DoesNotExist:
                pass

        # if not isinstance(request.user, AnonymousUser):
        #     try:
        #         client_config = ClientConfig.objects.prefetch_related('client').get(client__user=request.user)
        #         db, db_name = initialize_mongo_instance(client_config)
        #         request.mongodb, request.db_name = db, db_name
        #     except:
        #         return JsonResponse({'error': "MongoDB not configured for {}".format(request.user.username)}, status=501)
        # logging.info(request.user)
