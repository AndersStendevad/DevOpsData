from django.urls import include, path
from minitwit.views import public_timeline, user_timeline, login, register


urlpatterns = [
    path('', public_timeline, name = 'public_timeline'), # Now both '' and /public leads to the same page... a little inconsistent..
    path('public/', public_timeline, name = 'public_timeline'),
    path('<username>/', user_timeline, name = 'user_timeline'),
    path('login/', login, name='login'),
    path('register/', register, name='register')
]
