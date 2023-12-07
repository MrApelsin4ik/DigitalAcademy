from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('tasklist/', views.tasklist_view, name='tasklist'),
    path('', views.main, name='main'),
    path('logout/', views.logout_user, name='logout'),
    path('partner_profile/', views.partner_profile, name='partner_profile'),
    path('make_task/', views.make_task, name='make_task')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)