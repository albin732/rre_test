from django.urls import path
from . import views

urlpatterns = [

    path('check_view_permission/', views.CheckCanViewPremissionView.as_view(),
         name='check_view_permission'),
    path('check_add_permission/', views.CheckCanAddPremissionView.as_view(),
         name='check_add_permission'),

    path('user_api/view', views.UserList.as_view(), name='user_api_view'),
    path('user_api/add/', views.UserCreate.as_view(), name='user_api_create'),

    path('user_api_detail/<int:id>/view/', views.UserDetail.as_view(),
         name='user_api_detail_view'),
    path('user_api_detail/<int:id>/change/',
         views.UserChange.as_view(), name='user_api_detail_change'),
    path('user_api_detail/<int:id>/delete/',
         views.UserDelete.as_view(), name='user_api_detail_delete'),
    path('user_api_detail/<int:id>/patch/',
         views.UserPatch.as_view(), name='user_api_detail_patch'),



    #     path('customer_api', views.CustomerList.as_view(), name='customer_api_view'),
    #     path('customer_api/add/', views.CustomerList.as_view(), name='customer_api_add'),

    #     path('customerdetail_api/<int:id>/', views.CustomerDetail.as_view(),
    #          name='customerdetail_api_view'),
    #     path('customerdetail_api/<int:id>/change/',
    #          views.CustomerDetail.as_view(), name='customerdetail_api_change'),
    #     path('customerdetail_api/<int:id>/delete/',
    #          views.CustomerDetail.as_view(), name='customerdetail_api_delete'),
]
