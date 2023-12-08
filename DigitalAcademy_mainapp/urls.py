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
    path('make_task/', views.make_task, name='make_task'),
    path('profile/', views.profile, name='profile'),
    path('participant_profile/', views.participant_profile, name='participant_profile'),
    path('add_project/', views.add_project, name='add_project'),
    path('task_detail/<int:task_id>/', views.task_detail, name='task_detail'),
    path('task/', views.task, name='task'),
    path('chat/', views.chat, name='chat'),
    path('wallet/', views.wallet, name='wallet')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)