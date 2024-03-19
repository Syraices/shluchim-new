from django.shortcuts import render, redirect

from .forms import CouponForm
from .models import Coupon, CouponUsage

# Create your views here.
def index(request):
    coupons = Coupon.objects.all()
    form = CouponForm()
    couponlist = []
    for coupon in coupons:
        coupon_users = CouponUsage.objects.filter(coupon=coupon)
        # print(coupon_users)
        couponlist.append({'coupon': coupon, 'users': len(coupon_users)})

    # print(couponlist)
    # for coupon in couponlist:
    #     print("code")
    #     print(coupon['coupon'].active)

    return render(request, 'coupon/coupons.html', {'coupons': couponlist, 'form': form})

def add_coupon(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        form.save()
        return redirect('coupons')
    else:
        form = CouponForm()
        return render(request, 'coupon/add_coupon.html', {'form': form})