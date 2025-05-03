from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('favorite/add/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorite/remove/<int:product_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('favorites/', views.favorites_list, name='favorites_list'),

]
