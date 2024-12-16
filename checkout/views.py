from django.shortcuts import render, redirect
from django.http import JsonResponse
from shop.models import Product
from shop.views import get_cart
from django.contrib import messages


def checkout_view(request):
    cart = get_cart(request)
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = [{'product': p, 'quantity': cart[str(p.id)]} for p in products]
    total = sum(item['product'].price * item['quantity'] for item in cart_items)

    return render(request, 'checkout/checkout.html', {
        'cart_items': cart_items,
        'cart_total': total
    })


def create_order(request):
    if request.method == 'POST':
        # Получаем данные из формы
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        # Получаем корзину
        cart = get_cart(request)
        products = Product.objects.filter(id__in=cart.keys())

        # Здесь должна быть логика создания заказа
        # Например, создание модели Order

        # Очистка корзины после оформления заказа
        request.session['cart'] = {}

        return JsonResponse({
            'success': True,
            'message': 'Заказ успешно оформлен!'
        })

    return JsonResponse({
        'success': False,
        'message': 'Ошибка при оформлении заказа'
    }, status=400)

def checkout(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, 'Ваша корзина пуста!')
            return redirect('cart')

        # Очистка корзины после оформления заказа
        request.session['cart'] = {}
        request.session.modified = True

        # Добавление уведомления об успешном оформлении
        messages.success(request, f'Спасибо, {name}! Ваш заказ успешно оформлен.')

        return redirect('checkout_success')  # Страница с подтверждением

    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = [{'product': p, 'quantity': cart[str(p.id)]} for p in products]
    total_price = sum(item['product'].price * item['quantity'] for item in cart_items)

    return render(request, 'shop/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

def checkout_success(request):
    return render(request, 'shop/checkout_success.html')