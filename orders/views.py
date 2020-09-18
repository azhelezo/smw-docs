from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import OrderForm
from .models import Order, Signature
from users.models import User, Profile

@login_required
def order_new(request):
    form = OrderForm(request.POST or None)
    if form.is_valid():
        form.instance.requested_by = request.user
        form.instance.save()
        return redirect('pending_orders')
    return render(request, 'order_new.html', {'form': form})

@login_required
def my_orders(request):
    if request.user.profile.department == None:
        return render(request, 'contact_admin.html')
    order_list = Order.objects.filter(requested_by=request.user)
    paginator = Paginator(order_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'pending_orders.html',
        {'page': page, 'paginator': paginator}
    )

@login_required
def pending_orders(request):
    if request.user.profile.department == None:
        return render(request, 'contact_admin.html')
    if (
        (request.user.profile.is_pur) or
        (request.user.profile.is_fin) or
        (request.user.profile.is_gm)
        ):
        order_list = Order.objects.all()
    elif request.user.profile.is_hod:
        order_list = Order.objects.filter(department=request.user.profile.department)
    else:
        order_list = Order.objects.filter(requested_by=request.user)
    paginator = Paginator(order_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'pending_orders.html',
        {'page': page, 'paginator': paginator}
    )

@login_required
def order_item(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    context = {}
    if (request.user.profile.department == order.department) and request.user.profile.is_hod:
        context['is_hod'] = True
    context['is_pur'] = request.user.profile.is_pur
    context['is_fin'] = request.user.profile.is_fin
    context['is_gm'] = request.user.profile.is_gm
    context['order'] = order
    context['hod_approved'] = order.hod_signature.approved if order.hod_signature else None
    context['pur_approved'] = order.pur_signature.approved if order.pur_signature else None
    context['fin_approved'] = order.fin_signature.approved if order.fin_signature else None
    context['gm_approved'] = order.gm_signature.approved if order.gm_signature else None
    return render(request, 'order_item.html', context)


@login_required
def order_sign(request, order_id, signature_lvl, resolution):
    order = get_object_or_404(Order, pk=order_id)
    if (
        (signature_lvl == 'hod' and not request.user.profile.is_hod) or
        (signature_lvl == 'pur' and not request.user.profile.is_pur) or
        (signature_lvl == 'fin' and not request.user.profile.is_fin) or
        (signature_lvl == 'gm' and not request.user.profile.is_gm)
        ):
        return redirect('order', order_id)
    new_signature = Signature.objects.create(
            user=request.user,
            approved=resolution,
            win_username=request.META['USERNAME'],
            win_pcname=request.META['COMPUTERNAME']
        )
    if signature_lvl == 'hod':
        order.hod_signature = new_signature
    if signature_lvl == 'pur':
        order.pur_signature = new_signature
    if signature_lvl == 'fin':
        order.fin_signature = new_signature
    if signature_lvl == 'gm':
        order.gm_signature = new_signature
    order.save(force_update=True)
    return redirect('order', order_id)

