from django.urls import path
from .views import RegisterView, LoginView

urlpatterns = [
    path('api/register/', RegisterView.as_view()),
    path('api/login/', LoginView.as_view()),
]
