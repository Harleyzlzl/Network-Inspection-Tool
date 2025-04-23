from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommandTemplateViewSet, InspectionTaskViewSet, InspectionResultViewSet

router = DefaultRouter()
router.register(r'templates', CommandTemplateViewSet)
router.register(r'tasks', InspectionTaskViewSet)
router.register(r'results', InspectionResultViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 