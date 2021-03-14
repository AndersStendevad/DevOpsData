from django.urls import path, include

from . import views

urlpatterns = [
    path("", include("django_prometheus.urls"), name="django-prometheus"),
    path("msgs/<username>", views.UserMessagesView.as_view()),
    path("msgs/", views.MessagesView.as_view()),
    path("fllws/<username>", views.UserFollowersView.as_view()),
    path("register/", views.RegistrationView.as_view()),
    path("register", views.RegistrationView.as_view()),
    path("latest/", views.LatestView),
]
