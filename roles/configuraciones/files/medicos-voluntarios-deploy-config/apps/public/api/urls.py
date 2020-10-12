from django.urls import path

from .views import ConsultasAPIView, DocumentRootAPIView

urlpatterns = [
    path("consultas/", ConsultasAPIView.as_view(), name="consultas_endpoint"),
    path("", DocumentRootAPIView.as_view(), name="document_root_endpoint"),
]
