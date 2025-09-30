from django.urls import path
from .views import (
    RegisterView, LoginView, UserListView, UserMeView, 
    UserUpdateView, UserDeleteView, ChangePasswordView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/me/', UserMeView.as_view(), name='user-me'),
    path('users/me/update/', UserUpdateView.as_view(), name='user-update'),
    path('users/me/delete/', UserDeleteView.as_view(), name='user-delete'),
    path('users/me/change_password/', ChangePasswordView.as_view(), name='change-password'),
]





