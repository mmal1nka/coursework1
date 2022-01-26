from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.RegistrationTemplate, name='reg'),
    path('Registration', views.Registration, name='signUp'),
    path('encrypt', views.EncryptedTemplate, name='encrypt'),
    path('AuthEncMes', views.AuthEncMes, name='authEncMes'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
