from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls')),
    path('auth/', include('auth_app.urls')),
    path('jwt/', include('auth_app.jwt.urls')),
    path('api/', include('api.urls'))
]
