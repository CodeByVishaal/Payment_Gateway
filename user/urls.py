from django.urls import path
from .views import RegisterView, LoginView, UserTestAuthenticationView, AdminRegistration

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserTestAuthenticationView.as_view()),
    path('register/admin/', AdminRegistration.as_view()),
]
