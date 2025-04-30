from django.shortcuts import render, get_object_or_404
from .models import Category, Product


def index(request):
    # products = Product.objects.filter(category_id=category_id)
    products = Product.objects.all()
    categories = Category.objects.all()
    context = {'products': products, 'categories': categories}
    return render(request, 'shop/index.html', context)