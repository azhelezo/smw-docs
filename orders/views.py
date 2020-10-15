from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import OrderForm
from .models import Order
from users.models import User, Profile, Signature, LEVEL

@login_required
def order_new(request):
    form = OrderForm(request.POST or None)
    if form.is_valid():
        form.instance.requested_by = request.user
        form.instance.save()
        return redirect('pending_orders')
    return render(request, 'order_new.html', {'form': form})

@login_required
def order_edit(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.user != order.requested_by:
        return redirect('order', order_id)
    form = OrderForm(request.POST or None, instance=order)
    if form.is_valid():
        form.instance.save()
        return redirect('order', order_id)
    return render(request, 'order_new.html', {'form': form, 'order': order})

@login_required
def order_cancel(request, order_id, confirmed):
    order = get_object_or_404(Order, pk=order_id)
    if request.user != order.requested_by:
        return redirect('order', order_id)
    if confirmed == 'confirmed':
        order.declined = True
        order.save(force_update=True)
        return redirect('pending_orders')
    return render(request, 'order_cancel.html', {'order': order})

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
def order_printable(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'order_printable.html', {'order': order})

@login_required
def pending_orders(request):
    if request.user.profile.department == None:
        return render(request, 'contact_admin.html')
    if (
        (request.user.profile.is_pur) or
        (request.user.profile.is_fin) or
        (request.user.profile.is_gm)
        ):
        order_list = Order.objects.filter(declined=False)
    elif request.user.profile.is_hod:
        order_list = Order.objects.filter(department=request.user.profile.department, declined=False)
    else:
        order_list = Order.objects.filter(requested_by=request.user, declined=False)
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
    if request.user.profile.department == None:
        return render(request, 'contact_admin.html')
    if (
        (request.user.profile.is_pur) or
        (request.user.profile.is_fin) or
        (request.user.profile.is_gm)
        ):
        order_list = Order.objects.filter(declined=True)
    elif request.user.profile.is_hod:
        order_list = Order.objects.filter(department=request.user.profile.department, declined=True)
    else:
        order_list = Order.objects.filter(requested_by=request.user, declined=True)
    paginator = Paginator(order_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'declined_orders.html',
        {'page': page, 'paginator': paginator}
    )

@login_required
def order_item(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    hod_signature = order.signatures.filter(level='HOD').first()
    pur_signature = order.signatures.filter(level='PUR').first()
    fin_signature = order.signatures.filter(level='FIN').first()
    gm_signature = order.signatures.filter(level='GM').first()
    context = {
        'is_pur': request.user.profile.is_pur,
        'is_fin': request.user.profile.is_fin,
        'is_gm': request.user.profile.is_gm,
        'order': order,
        'declined': order.declined,
        'hod_approved': hod_signature.approved if hod_signature else None,
        'pur_approved': pur_signature.approved if pur_signature else None,
        'fin_approved': fin_signature.approved if fin_signature else None,
        'gm_approved': gm_signature.approved if gm_signature else None,
        'hod_name': hod_signature.user.get_full_name() if hod_signature else None,
        'pur_name': pur_signature.user.get_full_name() if pur_signature else None,
        'fin_name': fin_signature.user.get_full_name() if fin_signature else None,
        'gm_name': gm_signature.user.get_full_name() if gm_signature else None,
        'owner': True if order.requested_by == request.user else False
    }
    if (request.user.profile.department == order.department) and request.user.profile.is_hod:
        context['is_hod'] = True
    return render(request, 'order_item.html', context)

@login_required
def order_sign(request, order_id, signature_lvl, resolution):
    order = get_object_or_404(Order, pk=order_id)
    profile = request.user.profile
    print(signature_lvl == 'HOD')
    if (
            (signature_lvl.upper == 'HOD' and not profile.is_hod) or
            (signature_lvl.upper == 'PUR' and not profile.is_pur) or
            (signature_lvl.upper == 'FIN' and not profile.is_fin) or
            (signature_lvl.upper == 'GM' and not profile.is_gm)
        ) or (
            order.signatures.filter(level=signature_lvl.upper()).first() != None
        ) or (
            signature_lvl not in [x for x, y in LEVEL]
        ):
        return redirect('order', order_id)
    Signature.objects.create(
            user=request.user,
            order=order,
            level=signature_lvl.upper(),
            approved=resolution,
            win_username=request.META['USERNAME'],
            win_pcname=request.META['COMPUTERNAME']
        )
    if resolution == 'False':
        order.declined = True
        order.save(force_update=True)
    return redirect('order', order_id)
