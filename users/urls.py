from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from work import views as W
urlpatterns=[
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate_account'),
    path('activation',views.activation_view,name='activation'),
    path('activation/complete', views.activation_complete_view, name='activated'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('resume/', views.resume_view, name='resume_view'),
    path('load_professions/', views.load_professions, name='load_professions'),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

