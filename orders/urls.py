from django.contrib import admin
from django.urls import include, path
from orders import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.pending_orders, name='pending_orders'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('declined/', views.declined_orders, name='declined'),
    path('search/', views.pending_orders, name='search'),
    path('order/new/', views.order_new, name='order_new'),
    path('order/<int:order_id>', views.order_item, name='order'),
    path('order/<int:order_id>/printable/', views.order_printable, name='order_printable'),
    path('order/<int:order_id>/edit/', views.order_edit, name='order_edit'),
    path('order/<int:order_id>/cancel/<str:confirmed>', views.order_cancel, name='order_cancel'),
    path('order/<int:order_id>/<int:signature_lvl>/<str:resolution>', views.order_sign, name='order_sign'),
]