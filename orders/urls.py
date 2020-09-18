from django.contrib import admin
from django.urls import include, path
from orders import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.pending_orders, name='pending_orders'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('search/', views.pending_orders, name='search'),
    path('order/new/', views.order_new, name='order_new'),
    path('order/<int:order_id>', views.order_item, name='order'),
    path('order/<int:order_id>/<str:signature_lvl>/<str:resolution>', views.order_sign, name='order_sign'),
]