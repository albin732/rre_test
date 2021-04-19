from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('logout/', Logout.as_view()),
    path('clients/', ClientsView.as_view()),
    re_path(r'clients/q=(?:(?P<client>[\w-]+))?/$', ClientAutoComplete.as_view()),
    re_path(r'accounts/$', AccountAutoComplete.as_view()),
    path('client/add/', ClientAddView.as_view()),
    path('client/edit/<int:pk>/', ClientEditView.as_view()),
    path('client/<int:pk>/delete/', ClientDeleteView.as_view()),
    path('thresholds/', SystemSettings.as_view()),
    path('thresholds/update/', SystemSettingsUpdate.as_view()),
    path('rules/', RulesConfig.as_view()),
    path('rules/update/', RulesUpdate.as_view())
]
