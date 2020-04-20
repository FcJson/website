from django.contrib import admin
from django.urls import path, include
from laf import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('home/', views.home),
    path('lost/', views.lost),
    path('found/', views.found),
    path('upload/', views.upload),
    path('accounts/login/', views.login),
    path('accounts/register/', views.register),
    path('accounts/logout/', views.logout),
    path('accounts/change/', views.change),
    path('accounts/forget/', views.forget),
    path('captcha/', include('captcha.urls')),
    path('captcha/refresh/', views.refresh_captcha),
    path('email/captcha/', views.send_captcha),
    path('province/city/', views.get_cities)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
