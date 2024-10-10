from django.conf.urls.static import static
from django.conf import settings

from hiredup.urls import urlpatterns

urlpatterns = [

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
