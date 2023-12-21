from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

handler404 = 'users.views.custom_404'

urlpatterns = [
    path('admin-panel/', admin.site.urls),
    path('users/', include('users.urls')),
    path('admins/', include('admins.urls')),
    path('', include('accounts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)