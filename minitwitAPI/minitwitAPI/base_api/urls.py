from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('msgs', views.MessagesView.as_view()),
]