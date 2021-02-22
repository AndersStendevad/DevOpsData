from django.urls import include, path
from minitwit.views import public_timeline, user_timeline, login, register, timeline, logout


urlpatterns = [
    path('', timeline, name='timeline'),
    path('public/', public_timeline, name = 'public_timeline'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('<username>/', user_timeline, name = 'user_timeline'),

]
