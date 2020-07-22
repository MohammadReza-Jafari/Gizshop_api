from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('profile/', views.ManageUserView.as_view(), name='profile'),
    path('token/', views.GetAuthTokenView.as_view(), name='token'),
    path('get-active-code/', views.GetActivationCodeView.as_view(), name='get_active_code'),
    path('activate/<str:activation_code>/', views.ActivationView.as_view(), name='activate'),
    path('get-reset-code/', views.GetResetCodeView.as_view(), name='get_reset_code'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset_password'),
]
