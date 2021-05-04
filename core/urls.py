from django.urls import path
from . import views

urlpatterns = [

    path('user_api/view', views.UserList.as_view(), name='user_api_view'),
    path('user_api/add/', views.UserCreate.as_view(), name='user_api_create'),

    path('user_api_detail/<int:id>/view/', views.UserDetail.as_view(),
         name='user_api_detail_view'),
    path('user_api_detail/<int:id>/change/',
         views.UserChange.as_view(), name='user_api_detail_change'),
    path('user_api_detail/<int:id>/delete/',
         views.UserDelete.as_view(), name='user_api_detail_delete'),
    #     path('user_api_detail/<int:id>/patch/',
    #          views.UserPatch.as_view(), name='user_api_detail_patch'),
]
