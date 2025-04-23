from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VendorViewSet, DeviceTypeViewSet, DeviceViewSet

router = DefaultRouter()
router.register(r'vendors', VendorViewSet)
router.register(r'types', DeviceTypeViewSet)
router.register(r'', DeviceViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 