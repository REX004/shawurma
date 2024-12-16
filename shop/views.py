from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages
from .models import Cart, Product


def get_cart(request):
    return request.session.get('cart', {})


def save_cart(request, cart):
    request.session['cart'] = cart


def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product_detail.html', {'product': product})


def add_to_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        cart[product_id] = cart.get(product_id, 0) + 1
        request.session['cart'] = cart
        return JsonResponse({'message': 'Товар добавлен в корзину!'})


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1
    request.session['cart'] = cart
    return JsonResponse({'message': 'Товар добавлен в корзину!'})


def update_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = Cart.objects.get(user=request.user, product_id=product_id)
        if quantity > 0:
            cart.quantity = quantity
            cart.save()
            messages.success(request, 'Количество обновлено.')
        else:
            messages.error(request, 'Количество должно быть больше 0.')
    return redirect('cart')
def remove_from_cart(request, product_id):
    if request.method == 'POST':
        cart = get_cart(request)
        if str(product_id) in cart:
            del cart[str(product_id)]  # Удаляем товар из корзины
            save_cart(request, cart)
            return JsonResponse({'message': 'Товар удалён из корзины.'})
        else:
            return JsonResponse({'message': 'Товар не найден в корзине.'}, status=404)


def cart(request):
    cart = get_cart(request)
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = [{'product': p, 'quantity': cart[str(p.id)]} for p in products]
    total = sum(item['product'].price * item['quantity'] for item in cart_items)
    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total': total})
