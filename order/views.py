from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import OrderCreateForm
from .models import Order, OrderItem
from cart.cart import Cart
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
import base64
import hashlib
import json
from django.conf import settings
from django.urls import reverse



@login_required
def order_create(request):
    cart = Cart(request)

    # Проверка: если корзина пуста — не продолжаем
    if not cart or len(cart) == 0:
        messages.warning(request, 'Ваш кошик порожній.')
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user  # обязательная привязка пользователя
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity']
                )
            cart.clear()
            messages.success(request, f'Замовлення №{order.id} успішно створено!')
            return redirect('order:order_detail', order_id=order.id)
    else:
        form = OrderCreateForm()
    return render(request, 'order/order_create.html', {'form': form, 'cart': cart})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order/order_detail.html', {'order': order})


def generate_signature(private_key, data):
    combined = private_key + data + private_key
    return base64.b64encode(hashlib.sha1(combined.encode('utf-8')).digest()).decode('utf-8')


def order_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    data_dict = {
        "public_key": settings.LIQPAY_PUBLIC_KEY,
        "version": "3",
        "action": "pay",
        "amount": str(order.get_total_cost()),
        "currency": "UAH",
        "description": f"Оплата замовлення №{order.id}",
        "order_id": str(order.id),
        "sandbox": 1,  # убрать, если боевой режим
        "server_url": request.build_absolute_uri(reverse('order:payment_callback')),
        "result_url": request.build_absolute_uri(reverse('order:order_detail', args=[order.id]))
    }

    data_json = json.dumps(data_dict)
    data_encoded = base64.b64encode(data_json.encode('utf-8')).decode('utf-8')
    signature = generate_signature(settings.LIQPAY_PRIVATE_KEY, data_encoded)

    return render(request, 'order/order_payment.html', {
        'order': order,
        'liqpay_data': data_encoded,
        'liqpay_signature': signature,
        'liqpay_url': 'https://www.liqpay.ua/api/3/checkout/'
    })


@csrf_exempt
def payment_callback(request):
    if request.method != 'POST':
        return HttpResponse(status=405)

    data = request.POST.get('data')
    signature = request.POST.get('signature')

    if not data or not signature:
        return HttpResponse(status=400)

    # Проверка подписи
    expected_signature = base64.b64encode(
        hashlib.sha1(
            (settings.LIQPAY_PRIVATE_KEY + data + settings.LIQPAY_PRIVATE_KEY).encode('utf-8')
        ).digest()
    ).decode('utf-8')

    if signature != expected_signature:
        return HttpResponse('Invalid signature', status=400)

    # Декодируем данные
    decoded_data = json.loads(base64.b64decode(data).decode('utf-8'))
    order_id = decoded_data.get('order_id')
    status = decoded_data.get('status')

    if status in ['success', 'sandbox', 'wait_accept']:
        from .models import Order
        try:
            order = Order.objects.get(id=order_id)
            order.is_paid = True
            order.save()
        except Order.DoesNotExist:
            return HttpResponse('Order not found', status=404)

    return HttpResponse('OK')