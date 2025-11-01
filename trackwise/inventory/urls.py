from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),
    path('add/', views.product_add, name='product_add'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('<int:pk>/increase/', views.increase_stock, name='increase_stock'),
    path('<int:pk>/decrease/', views.decrease_stock, name='decrease_stock'),
]