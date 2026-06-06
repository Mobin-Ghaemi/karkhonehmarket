from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('listings/', views.listings, name='listings'),
    path('listings/<int:pk>/', views.listing_detail, name='listing_detail'),
    path('category/<str:category>/', views.category_page, name='category'),
]
