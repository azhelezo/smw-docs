from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from .decorators import user_can_access
from .forms import OrderForm
from .models import Order
from users.models import User, Profile, Signature, LEVEL, LEVEL_VIEW_ALL

def get_order_list(request, declined):
    user_access = [int(x) for x in request.user.profile.sign_as]
    if [x for x in user_access if x in LEVEL_VIEW_ALL]:
        order_list = Order.objects.filter(declined=declined)
    elif 1 in user_access:
        order_list = Order.objects.filter(department=request.user.profile.department, declined=declined)
    else:
        order_list = Order.objects.filter(requested_by=request.user, declined=declined)
    return order_list

@login_required
def order_new(request):
    form = OrderForm(request.POST or None)
    if form.is_valid():
        form.instance.requested_by = request.user
        form.instance.save()
        return redirect('pending_orders')
    return render(request, 'order_new.html', {'form': form})

@login_required
@user_can_access
def order_edit(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    form = OrderForm(request.POST or None, instance=order)
    if form.is_valid():
        form.instance.save()
        return redirect('order', order_id)
    return render(request, 'order_new.html', {'form': form, 'order': order})

@login_required
@user_can_access
def order_cancel(request, order_id, confirmed):
    order = get_object_or_404(Order, pk=order_id)
    if confirmed == 'confirmed':
        order.declined = True
        order.save(force_update=True)
        return redirect('pending_orders')
    return render(request, 'order_cancel.html', {'order': order})

@login_required
def my_orders(request):
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
@user_can_access
def order_printable(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'order_printable.html', {'order': order})

@login_required
def pending_orders(request):
    order_list = get_order_list(request=request, declined=False)
    paginator = Paginator(order_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'pending_orders.html',
        {'page': page, 'paginator': paginator}
    )

@login_required
def declined_orders(request):
    order_list = get_order_list(request=request, declined=True)
    paginator = Paginator(order_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'declined_orders.html',
        {'page': page, 'paginator': paginator}
    )

@login_required
@user_can_access
def order_item(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    context = {
        'order': order,
        'declined': order.declined,
        'is_owner': True if order.requested_by == request.user else False,
        'signature_levels': [x for x, y in LEVEL],
        'signatures': {}
    }
    for level, level_name in LEVEL:
        signature = order.signatures.filter(level=level).first()
        context['signatures'][level] = {
            'signature': signature,
            'signature_name': level_name,
            'user_is_level': str(level) in repr(request.user.profile.sign_as),
        }
        if signature is not None:
            context['signatures'][level]['signed_by'] = signature.user.get_full_name()
            context['signatures'][level]['approved'] = signature.approved
        else:
            context['signatures'][level]['signed_by'] = None
            context['signatures'][level]['approved'] = None
    return render(request, 'order_item.html', context)

@login_required
@user_can_access
def order_sign(request, order_id, signature_lvl, resolution):
    order = get_object_or_404(Order, pk=order_id)
    profile = request.user.profile
    if (
            str(signature_lvl) not in repr(profile.sign_as)
        ) or (
            order.signatures.filter(level=signature_lvl).first() != None
        ) or (
            signature_lvl not in [x for x, y in LEVEL]
        ) or (
            order.declined
        ):
        return redirect('order', order_id)
    Signature.objects.create(
            user=request.user,
            order=order,
            level=signature_lvl,
            approved=resolution,
            win_username=request.META['USERNAME'],
            win_pcname=request.META.get('COMPUTERNAME', '*nix')
        )
    if resolution == 'False':
        order.declined = True
        order.save(force_update=True)
    elif not order.declined and order.signatures.count() == 4:
        order.all_signed = True
        order.save(force_update=True)
    return redirect('order', order_id)
