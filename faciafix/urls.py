"""
URL configuration for faciafix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
# from accounts.views import ImageProcessingView
from accounts.views import CustomUserDetailView, CustomUserUpdateView
from accounts.views import  DoctorPatientsView, CustomRegisterView,CustomLoginView, CustomUserDetailView, CustomUserUpdateView, SelectDoctorView

from accounts.views import ProgressView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('user/', CustomUserDetailView.as_view(), name='user-detail'),
    path('user/edit/', CustomUserUpdateView.as_view(), name='user-edit'),
    path('login/', CustomLoginView.as_view(), name='custom_login'),
    path('register/', CustomRegisterView.as_view(), name='custom_Register'),
    path('select-doctor/', SelectDoctorView.as_view(), name='select-doctor'),
    path('progress/', ProgressView.as_view(), name='progress'),
    path('doctor/patients/', DoctorPatientsView.as_view(), name='doctor-patients'),

    ]
    

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)