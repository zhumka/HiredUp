from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from work.views import home_view
from . import views

urlpatterns = [
    path('',home_view,name='home'),
    path('vacancy/<int:vacancy_id>/', views.vacancy_detail_view, name = 'vacancy_detail'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
