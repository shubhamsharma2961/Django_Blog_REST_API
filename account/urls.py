from django.contrib import admin
from django.urls import path
from account.views import RegisterView, loginView, UserProfileView, UserProfileFilterSearchView, UserCRUDView, CurrentUserPofileView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', loginView.as_view()),
    path('profile/', UserProfileView.as_view()),
    path('filter-search-profiles/', UserProfileFilterSearchView.as_view()),
    path('user-crud/', UserCRUDView.as_view()),
    path('user-crud/<int:pk>/', UserCRUDView.as_view()),
    path('current-user-profile/', CurrentUserPofileView.as_view())
]
