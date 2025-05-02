from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from blog.models import Post


def product_list(request, category_slug=None):
    category = None
    search_query = request.GET.get('q', '').strip()
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug and not search_query:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    blog_posts = Post.objects.filter(published=True).order_by('-created_at')[:3]

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'category': category,
        'selected_category': category.id if category else '',
        'search_query': search_query,
        'blog_posts': blog_posts,
    }

    return render(request, 'shop/product_list.html', context)

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return render(request, 'shop/product_detail.html', {'product': product})

