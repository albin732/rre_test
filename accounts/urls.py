
from django.urls import path
from .view.logs import Login, Logout
from .view.dashboard import AdminDashboard, SubAdminDashboard, CustomerDashboard
from .view.registeration import SignUp

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('admin_dashboard/', AdminDashboard.as_view(), name='admin_dashboard'),
    path('sub_admin_dashboard/', SubAdminDashboard.as_view(),
         name='sub_admin_dashboard'),
    path('customer_dashboard/', CustomerDashboard.as_view(),
         name='customer_dashboard'),
]
