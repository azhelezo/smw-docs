from django.contrib import admin
from django.urls import include, path
from orders import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.pending_index, name='pending_index'),
    path('approved/', views.pending_index, name='approved_index'),
    path('declined/', views.pending_index, name='declined_index'),
    path('search/', views.pending_index, name='search'),
    path('order/<int:order_id>', views.order_item, name='order'),
]