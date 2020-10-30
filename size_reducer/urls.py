from django.urls import path
from . import views

app_name = 'size_reducer'
urlpatterns = [
    path('', views.MainView.as_view(), name='all'),
    path('delete/', views.ImageDelete, name='delete'),
    path('zip/', views.MakeZip.as_view(), name='zip'),
    path('data_delete/', views.data_delete, name='data_delete'),
]
