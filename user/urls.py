from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('profile/', views.ManageUserView.as_view(), name='profile'),
    path('token/', views.GetAuthTokenView.as_view(), name='token')
]