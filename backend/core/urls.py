from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, SystemSettingViewSet, AuditLogViewSet,
    CustomAuthToken, DashboardView
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'settings', SystemSettingViewSet)
router.register(r'audit-logs', AuditLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomAuthToken.as_view(), name='api-token-auth'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
] 