from django.urls import path

from . import views

urlpatterns = [
    path('', views.OrderListView.as_view(), name='order-list'),
    path('order-create/', views.OrderCreateView.as_view(), name='order-create'),
    path('order-success/', views.SuccessTemplateView.as_view(), name='order-success'),
    path('order-canceled/', views.CanceledTemplateView.as_view(), name='order-canceled'),
]