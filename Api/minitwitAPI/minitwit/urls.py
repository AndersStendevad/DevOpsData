from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('msgs/<username>', views.UserMessagesView.as_view()),
    path('msgs/', views.MessagesView.as_view()),
    path('fllws/<username>', views.UserFollowersView.as_view()),
    path('register/', views.RegistrationView.as_view()),
    path('latest/', views.LatestView.as_view()),
]