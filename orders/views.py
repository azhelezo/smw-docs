from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import OrderForm
from .models import Order, User

def pending_index(request):
    order_list = Order.objects.all()
    paginator = Paginator(order_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'pending_index.html',
        {'page': page, 'paginator': paginator}
    )

def order_item(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(
        request,
        'order_item.html',
        {'order': order})

