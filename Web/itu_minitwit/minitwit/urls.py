from django.urls import include, path
from minitwit.views import (
    public_timeline,
    user_timeline,
    login,
    register,
    logout,
    timeline,
    follow_user,
    unfollow_user,
)


urlpatterns = [
    path(
        "", public_timeline, name="public_timeline"
    ),  # Now both '' and /public leads to the same page... a little inconsistent..
    path("", include("django_prometheus.urls"), name="django-prometheus"),
    path("public/", public_timeline, name="public_timeline"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("register/", register, name="register"),
    path("timeline/", timeline, name="timeline"),
    path("<username>/follow", follow_user, name="follow_user"),
    path("<username>/unfollow", unfollow_user, name="unfollow_user"),
    path("<username>/", user_timeline, name="user_timeline"),
]
