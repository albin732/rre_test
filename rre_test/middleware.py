import logging
from re import sub

from django.http import JsonResponse

from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin

from rest_framework.authtoken.models import Token
from core.models import Profile

# from utils.mongo_utils import initialize_mongo_instance
# from core.models import ClientConfig

# create token
# python manage.py drf_create_token user_name


class MongoDBSelectorMiddleware(MiddlewareMixin):

    def process_request(self, request):
        header_token = request.META.get('HTTP_AUTHORIZATION', None)
        # header_token = 'b436c73f2cef4faaab0172f6943869ca89cfff38' for user q
        # Generated token bd1d969b932db8ad3760baf57661b33ac62af155 for user a1@a.com
        # Generated token 169558d53cf231ebd11e879ae6e293fcfb19bbaa for user c1@c.com
        if header_token is not None:
            try:
                token = sub('Token ', '', request.META.get(
                    'HTTP_AUTHORIZATION', None))
                token_obj = Token.objects.get(key=token)
                user = token_obj.user
                request.user = user
                # user_permissions = request.user.profile.all_permissions()
                user_permissions = Profile.profiles.all_permissions(
                    request.user)
                print('permissions...')
                print(user_permissions)
                request.permissions = [
                    i.codename for i in user_permissions] if user.profile.role else []

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
