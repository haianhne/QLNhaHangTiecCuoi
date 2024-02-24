"""
URL configuration for managerapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

import debug_toolbar
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from oauth2_provider.views import TokenView, AuthorizationView, RevokeTokenView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from app import views


schema_view = get_schema_view(
    openapi.Info(
        title="NhaHangTiecCuoi API",
        default_version='v1',
        description="APIs for Quan Ly Nha Hang Tiec Cuoi",
        contact=openapi.Contact(email="1951052009anh@ou.edu.vn"),
        license=openapi.License(name="Nguyễn Duy Hải Anh"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # ... the rest of your URLconf goes here ...
    '%s/app/static/'
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns = [
    path('', include('app.urls')),
    path('admin/', admin.site.urls),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path('o/token/', TokenView.as_view(), name='token'),
    path('o/authorize/', AuthorizationView.as_view(), name='authorize'),
    path('o/revoke_token/', RevokeTokenView.as_view(), name='revoke-token'),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('token/', TokenView.as_view(), name='token'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('__debug__/', include(debug_toolbar.urls)),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0),
            name='schema-json'),
    re_path(r'^swagger/$',
            schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'),
    re_path(r'^redoc/$',
            schema_view.with_ui('redoc', cache_timeout=0),
            name='schema-redoc')
]
