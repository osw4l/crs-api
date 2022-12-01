from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Booking Engine Api",
        default_version='v1',
        description="Project built by osw4l",
        contact=openapi.Contact(email="ioswxd@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('booking/', include('apps.booking.urls')),
    path('', schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
]
