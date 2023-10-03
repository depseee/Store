from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy, reverse
from django.conf import settings

from orders.forms import OrderForm
from .models import Order


class SuccessTemplateView(TemplateView):
    """Сообщение об успешном заказе"""
    template_name = 'orders/success.html'

    def get_context_data(self, **kwargs):
        context = super(SuccessTemplateView, self).get_context_data()
        context['title'] = 'Store - Спасибо за заказ!'
        return context


class CanceledTemplateView(TemplateView):
    """Сообщение об ошибке заказа"""
    template_name = 'orders/cancel.html'


class OrderListView(ListView):
    """Список заказов"""
    template_name = 'orders/orders.html'
    queryset = Order.objects.all()
    ordering = ('-created',)

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data()
        context['title'] = 'Store - Заказы'
        return context

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)


class OrderCreateView(CreateView):
    """Создание заказа"""
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('order-create')

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data()
        context['title'] = 'Store - Оформление заказа'
        return context

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)
