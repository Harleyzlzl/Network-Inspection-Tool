from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReportViewSet, ReportTemplateViewSet

router = DefaultRouter()
router.register(r'templates', ReportTemplateViewSet)
router.register(r'', ReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 