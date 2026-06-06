from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/', views.register_view, name='register'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/listings/', views.my_listings, name='my_listings'),
    path('dashboard/listings/new/', views.post_listing, name='post_listing'),
    path('dashboard/listings/<int:pk>/delete/', views.delete_listing, name='delete_listing'),
    path('dashboard/profile/', views.edit_profile, name='edit_profile'),
    path('dashboard/consultation/', views.consultation, name='consultation'),
]
