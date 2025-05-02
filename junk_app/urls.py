from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('rooms/', views.rooms_index, name='rooms_index'),
    path('rooms/new/', views.rooms_new, name='rooms_new'),
    path('rooms/create/', views.rooms_create, name='rooms_create'),
    path('rooms/<int:room_id>/', views.rooms_detail, name='rooms_detail'),
    path('rooms/<int:room_id>/edit/', views.rooms_edit, name='rooms_edit'),
    path('rooms/<int:room_id>/update/', views.rooms_update, name='rooms_update'),
    path('rooms/<int:room_id>/delete/', views.rooms_delete, name='rooms_delete'),
    path('items/', views.items_index, name='items_index'),
    path('items/new/', views.items_new, name='items_new'),
    path('items/create/', views.items_create, name='items_create'),
    path('items/<int:item_id>/', views.items_detail, name='items_detail'),
    path('items/<int:item_id>/edit/', views.items_edit, name='items_edit'),
    path('items/<int:item_id>/update/', views.items_update, name='items_update'),
    path('items/<int:item_id>/delete/', views.items_delete, name='items_delete'),
]