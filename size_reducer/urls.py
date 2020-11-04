from django.urls import path
from . import views

app_name = 'size_reducer'
urlpatterns = [
    path('', views.MainView.as_view(), name='all'),
    path('zip/', views.MakeZip.as_view(), name='zip'),
    path('data_delete/<str:tabid>', views.data_delete, name='data_delete'),
]
