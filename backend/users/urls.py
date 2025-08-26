from django.urls import path
from .views import RegisterView, LoginView, UserListView, UserMeView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/me/', UserMeView.as_view(), name='user-me'),
]
