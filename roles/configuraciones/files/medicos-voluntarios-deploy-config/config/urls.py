"""medicos_voluntarios URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from apps.common.views import LandingView, MenuView, SuccessView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("menu/", MenuView.as_view(), name="menu"),
    path("", LandingView.as_view(), name="landing"),
    path("success/", SuccessView.as_view(), name="success"),
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("api/v1/", include(("apps.public.api.urls", "public"), namespace="api")),
    path("consulta/", include("apps.consultas.urls", namespace="consulta")),
    path("medico/", include("apps.medicos.urls", namespace="medico")),
    path("minsa/", include("apps.minsa.urls", namespace="minsa")),
    path("paciente/", include("apps.pacientes.urls", namespace="paciente")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
