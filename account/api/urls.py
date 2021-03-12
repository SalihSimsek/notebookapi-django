from django.urls import path
from .views import *


urlpatterns = [
    path('login/',ObtainAuthTokenView.as_view(),name='login'),
    path('register/',registration_view,name='register'),
    path('detail/',account_view,name='detail'),
    path('update/',update_account,name='update'),
    path('logout/',Logout.as_view(),name='logout'),
]