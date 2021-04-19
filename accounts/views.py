from rest_framework.response import Response

from core.views import FEView


class UserPermissions(FEView):

    def get(self, request):
        return Response({'permissions': request.permissions})
