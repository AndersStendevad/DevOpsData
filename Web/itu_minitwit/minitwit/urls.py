from django.urls import include, path
from minitwit.views import (
    public_timeline,
    user_timeline,
    login,
    register,
    logout,
    timeline,
)


urlpatterns = [
    path(
        "", timeline, name="timeline"
    ),  # Now both '' and /public leads to the same page... a little inconsistent..
    path("public/", public_timeline, name="public_timeline"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("register/", register, name="register"),
    path("timeline/", timeline, name="timeline"),
    path("<username>/", user_timeline, name="user_timeline"),
]
