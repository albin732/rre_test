
from django.urls import path
from .view.logs import Login, Logout
from .view.registeration import SignUp

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
]
