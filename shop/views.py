from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Category, Product


def index(request):
    # products = Product.objects.filter(category_id=category_id)
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {'products': products, 'categories': categories}
    return render(request, 'index.html', context)


def product_list(request):
    category_id = request.GET.get('category')
    search_query = request.GET.get('q')

    products = Product.objects.filter(in_stock=True)
    categories = Category.objects.all()

    if category_id:
        products = products.filter(category_id=category_id)

    if search_query:
        products = products.filter(Q(name__icontains=search_query))

    paginator = Paginator(products, 6)  # 6 товаров на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_id,
        'search_query': search_query,
    }

    return render(request, 'shop/product_list.html', context)