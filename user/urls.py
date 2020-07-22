from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('profile/', views.ManageUserView.as_view(), name='profile'),
    path('token/', views.GetAuthTokenView.as_view(), name='token'),
    path('get-active-code/', views.GetActivationCodeView.as_view(), name='get_active_code'),
    path('activate/<str:activation_code>/', views.ActivationView.as_view(), name='activate'),
]
