from django.shortcuts import render, redirect, get_object_or_404
from .models import CartItem
from shop.models import Product
from django.contrib.auth.decorators import login_required


@login_required
def cart_detail(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.get_total_price() for item in items)
    return render(request, 'cart/cart.html', {'items': items, 'total': total})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        item.quantity += 1
    item.save()
    return redirect('cart:detail')


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect('cart:detail')

