from django.contrib import admin
from django.urls import include, path
from orders import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include('orders.urls')),
]
