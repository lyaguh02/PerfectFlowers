import random

from django.contrib import messages
from django.contrib.auth import login
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from shop.cart import Cart
from shop.forms import ProductQuantityForm, NewUserForm
from shop.models import Product, Category, ViewCount
from pytils.translit import slugify


def index(request):
    """
    Отображение главной страницы
    """
    popular_products = random.sample(list(set(Product.objects.all())), 6)
    return render(request, 'index.html', {'popular_products': popular_products})


def products_list(request, slug=None):
    """
    Отображение списка всех товаров или по категориям
    """
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    if slug:
        category = get_object_or_404(Category, slug=slug)
        products = products.filter(category=category)
    return render(request,
                  'products/products_list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


def product_detail(request, slug):
    """
    Детальный показ товара
    """
    product = get_object_or_404(Product, slug=slug)

    if not request.user.is_anonymous:
        # получаем или создаем запись о просмотре товара для данного пользователя
        ViewCount.objects.get_or_create(product=product, username=request.user)

    return render(request, 'products/product_detail.html', {'product': product})


def search(request):
    """
    Отображение списка товаров по запросу
    """
    query = request.GET.get("query", 'Пустой запрос').strip()  # strip() убирает пробелы в начале и в конце

    # фильтрация по названию и ссылке
    slug_query = slugify(query)  # конвертируем в ссылку, так как sqlite не умеет фильтровать по кириллице
    products = Product.objects.all().filter(Q(name__icontains=slug_query) | Q(slug__icontains=slug_query))
    return render(request,
                  'products/products_list.html',
                  {'products': products,
                   'custom_title': f'Поиск ({query})'})


def add_to_cart(request, product_id, quantity=1, update_quantity=False):
    """
    Ссылка на добавление товара в корзину или его обновление
    """
    if request.method == "POST":
        quantity = int(ProductQuantityForm(request.POST)['quantity'].value())
        update_quantity = True
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product, quantity=quantity, update_quantity=update_quantity)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # редирект на эту же страницу


def remove_from_cart(request, product_id):
    """
    Ссылка на удаление товара из корзины
    """
    Cart(request).remove(product_id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # редирект на эту же страницу


def clear_cart(request):
    """
    Ссылка на очистку корзины товаров
    """
    Cart(request).clear()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  # редирект на эту же страницу


def cart_detail(request):
    """
    Отображение списка товаров корзины
    """
    cart = Cart(request)
    for item in cart:
        item['quantity_form'] = ProductQuantityForm(initial={'quantity': item['quantity']})
    return render(request, 'cart/cart_detail.html',
                  {'cart': cart})


def order_processed(request):
    """
    Отображение завершения покупки
    """
    Cart(request).clear()
    return render(request, 'cart/order_processed.html')


def register(request):
    """
    Отображение регистрации
    """
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Успешная регистрация!")
            return redirect('home')
        messages.error(request, "Неудачная попытка регистрации. Неправильная информация")

    form = NewUserForm()
    return render(request, 'registration/register.html', {'register_form': form})


def profile(request):
    """
    Отображение профиля
    """
    return render(request, 'registration/profile.html')
