from django.urls import path
from . import views

urlpatterns = [

    path('check_view_permission/', views.CheckCanViewPremissionView.as_view(),
         name='check_view_permission'),
    path('check_add_permission/', views.CheckCanAddPremissionView.as_view(),
         name='check_add_permission'),

    path('customer_api', views.CustomerList.as_view(), name='customer_api_view'),
    path('customer_api/add/', views.CustomerList.as_view(), name='customer_api_add'),

    path('customerdetail_api/<int:id>/', views.CustomerDetail.as_view(),
         name='customerdetail_api_view'),
    path('customerdetail_api/<int:id>/change/',
         views.CustomerDetail.as_view(), name='customerdetail_api_change'),
    path('customerdetail_api/<int:id>/delete/',
         views.CustomerDetail.as_view(), name='customerdetail_api_delete'),
]
