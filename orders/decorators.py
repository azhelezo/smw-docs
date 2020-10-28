from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from .models import Order, User
from users.models import Profile, LEVEL_VIEW_ALL

def user_can_access(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        profile = user.profile
        user_access = [int(x) for x in request.user.profile.sign_as]
        if profile.department == None:
            return render(request, 'contact_admin.html')
        order = Order.objects.get(pk=kwargs['order_id'])
        if (
                user == order.requested_by
            ) or (
                (profile.department == order.department) and 1 in user_access
            ) or (
                [x for x in user_access if x in LEVEL_VIEW_ALL]
            ):
            return function(request, *args, **kwargs)
        else:
            return redirect('pending_orders')
    return wrap