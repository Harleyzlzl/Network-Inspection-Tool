from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# 修改管理站点标题
admin.site.site_header = '网络自动化巡检系统'
admin.site.site_title = '网络巡检管理'
admin.site.index_title = '管理后台'

schema_view = get_schema_view(
    openapi.Info(
        title="网络自动化巡检工具 API",
        default_version='v1',
        description="网络系统自动化巡检工具API文档",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # 根路径重定向到Swagger页面
    path('', RedirectView.as_view(url='/admin/', permanent=False)),
    
    path('admin/', admin.site.urls),
    path('api/v1/devices/', include('devices.urls')),
    path('api/v1/inspections/', include('inspections.urls')),
    path('api/v1/reports/', include('reports.urls')),
    path('api/v1/core/', include('core.urls')),
    
    # API文档
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# 在开发环境中添加媒体文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 