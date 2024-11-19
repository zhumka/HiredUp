from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from work.views import home_view
from . import views

urlpatterns = [
    path('',home_view,name='home'),
    path('vacancy/<int:vacancy_id>/', views.vacancy_detail_view, name = 'vacancy_detail'),
    path('vacancy/<int:vacancy_id>/apply/', views.apply_to_vacancy, name='apply_to_vacancy'),
    path('applications/', views.applications_view, name='applications'),
    path('application/<int:application_id>/', views.application_detail_view, name='application_detail'),
    path('application/<int:application_id>/update_status/', views.update_application_status, name='update_application_status'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
