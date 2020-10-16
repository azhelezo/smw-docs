from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from .models import Order, User
from users.models import Profile

def user_can_access(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        profile = user.profile
        if profile.department == None:
            return render(request, 'contact_admin.html')
        order = Order.objects.get(pk=kwargs['order_id'])
        if (
                user == order.requested_by
            ) or (
                (profile.department == order.department) and profile.is_hod
            ) or (
                profile.is_pur
            ) or (
                profile.is_fin
            ) or (
                profile.is_gm
            ):
            return function(request, *args, **kwargs)
        else:
            return redirect('pending_orders')
    return wrap