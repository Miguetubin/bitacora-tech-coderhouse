from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('acerca-de/', views.about, name='about'),
    path('publicaciones/nueva/', views.post_create, name='post_create'),
    path('publicaciones/<int:pk>/', views.post_detail, name='post_detail'),
    path('publicaciones/<int:pk>/editar/', views.post_update, name='post_update'),
    path('publicaciones/<int:pk>/eliminar/', views.post_delete, name='post_delete'),
]
