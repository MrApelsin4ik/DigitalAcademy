from django.urls import path

from . import views

urlpatterns = [
    path('', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('tasklist/', views.tasklist_view, name='tasklist'),
    path('main/', views.main, name='main'),
]


