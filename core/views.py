from django.shortcuts import render, get_object_or_404
from .models import Listing, CATEGORY_CHOICES, STATUS_CHOICES


def home(request):
    featured = Listing.objects.filter(is_featured=True)[:6]
    recent = Listing.objects.all()[:8]
    stats = {
        'land': Listing.objects.filter(category='land').count(),
        'factory': Listing.objects.filter(category='factory').count(),
        'machinery': Listing.objects.filter(category='machinery').count(),
        'import': Listing.objects.filter(category='import').count(),
        'export': Listing.objects.filter(category='export').count(),
        'product': Listing.objects.filter(category='product').count(),
        'electricity': Listing.objects.filter(category='electricity').count(),
        'water': Listing.objects.filter(category='water').count(),
    }
    stats['all'] = sum(stats.values())
    stats['sale'] = Listing.objects.filter(status='sale').count()
    return render(request, 'core/home.html', {
        'featured': featured,
        'recent': recent,
        'stats': stats,
    })


def listings(request):
    category = request.GET.get('category', '')
    status = request.GET.get('status', '')
    search = request.GET.get('q', '')

    qs = Listing.objects.all()
    if category:
        qs = qs.filter(category=category)
    if status:
        qs = qs.filter(status=status)
    if search:
        qs = qs.filter(title__icontains=search) | qs.filter(location__icontains=search)

    return render(request, 'core/listings.html', {
        'listings': qs,
        'categories': CATEGORY_CHOICES,
        'active_category': category,
        'active_status': status,
        'search': search,
    })


def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    related = Listing.objects.filter(category=listing.category).exclude(pk=pk)[:4]
    return render(request, 'core/listing_detail.html', {
        'listing': listing,
        'related': related,
    })


def products(request):
    qs = Listing.objects.all()
    stats = {
        'all': qs.count(),
        'land': qs.filter(category='land').count(),
        'factory': qs.filter(category='factory').count(),
        'machinery': qs.filter(category='machinery').count(),
        'import': qs.filter(category='import').count(),
        'export': qs.filter(category='export').count(),
        'product': qs.filter(category='product').count(),
        'sale': qs.filter(status='sale').count(),
        'rent': qs.filter(status='rent').count(),
        'buy': qs.filter(status='buy').count(),
    }
    return render(request, 'core/products.html', {
        'listings': qs,
        'stats': stats,
        'categories': CATEGORY_CHOICES,
        'statuses': STATUS_CHOICES,
    })


def category_page(request, category):
    cat_map = dict(CATEGORY_CHOICES)
    cat_label = cat_map.get(category, '')
    qs = Listing.objects.filter(category=category)
    return render(request, 'core/category.html', {
        'listings': qs,
        'category': category,
        'category_label': cat_label,
    })
