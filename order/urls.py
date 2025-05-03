from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('payment/<int:order_id>/', views.order_payment, name='order_payment'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),
    path('', views.order_list, name='order_list'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('create/', views.order_create, name='order_create'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
]
