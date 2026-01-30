
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('core.urls', 'core'), namespace='core')),
    # path('accounts/', include('accounts.urls')),
    # path('tickets/', include('tickets.urls')),
    # path('comments/', include('comments.urls')),
]
