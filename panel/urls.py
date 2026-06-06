from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='panel_dashboard'),
    path('users/', views.users_list, name='panel_users'),
    path('users/<int:pk>/', views.user_detail, name='panel_user_detail'),
    path('listings/', views.listings_list, name='panel_listings'),
    path('listings/<int:pk>/action/', views.listing_toggle, name='panel_listing_toggle'),
    path('categories/', views.categories_list, name='panel_categories'),
    path('categories/<int:pk>/edit/', views.category_edit, name='panel_category_edit'),
    path('visits/', views.visits_view, name='panel_visits'),
    path('consultations/', views.consultations_view, name='panel_consultations'),
]
