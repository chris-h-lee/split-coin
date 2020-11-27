from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", include('base.urls')),
    path('admin/', admin.site.urls),
    path("accounts/", include("allauth.urls")),
]# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)