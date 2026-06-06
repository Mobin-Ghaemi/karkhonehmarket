from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from core.models import Listing, Category, SiteVisit, CATEGORY_CHOICES
from accounts.models import UserProfile, ConsultationRequest
from django.db.models import Count
from django.contrib import messages


@staff_member_required(login_url='/auth/login/')
def dashboard(request):
    today = timezone.now().date()
    week_ago = today - timedelta(days=6)

    total_users = User.objects.count()
    new_users_today = User.objects.filter(date_joined__date=today).count()
    total_listings = Listing.objects.count()
    active_listings = Listing.objects.filter(is_active=True).count()
    featured_listings = Listing.objects.filter(is_featured=True).count()
    total_consultations = ConsultationRequest.objects.count()
    pending_consultations = ConsultationRequest.objects.filter(status='pending').count()

    today_visit = SiteVisit.objects.filter(date=today).first()
    today_visits = today_visit.visits if today_visit else 0
    today_unique = today_visit.unique_visits if today_visit else 0
    total_visits = sum(v.visits for v in SiteVisit.objects.all())

    chart_labels = []
    chart_visits = []
    chart_unique = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        v = SiteVisit.objects.filter(date=d).first()
        chart_labels.append(d.strftime('%m/%d'))
        chart_visits.append(v.visits if v else 0)
        chart_unique.append(v.unique_visits if v else 0)

    categories = Category.objects.all()
    recent_listings = Listing.objects.order_by('-created_at')[:8]
    recent_users = User.objects.order_by('-date_joined')[:5]

    return render(request, 'panel/dashboard.html', {
        'total_users': total_users,
        'new_users_today': new_users_today,
        'total_listings': total_listings,
        'active_listings': active_listings,
        'featured_listings': featured_listings,
        'total_consultations': total_consultations,
        'pending_consultations': pending_consultations,
        'today_visits': today_visits,
        'today_unique': today_unique,
        'total_visits': total_visits,
        'chart_labels': chart_labels,
        'chart_visits': chart_visits,
        'chart_unique': chart_unique,
        'categories': categories,
        'recent_listings': recent_listings,
        'recent_users': recent_users,
    })


@staff_member_required(login_url='/auth/login/')
def users_list(request):
    q = request.GET.get('q', '')
    users = User.objects.select_related('profile').order_by('-date_joined')
    if q:
        users = users.filter(username__icontains=q) | users.filter(
            email__icontains=q) | users.filter(first_name__icontains=q)
    return render(request, 'panel/users.html', {'users': users, 'q': q})


@staff_member_required(login_url='/auth/login/')
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    profile, _ = UserProfile.objects.get_or_create(user=user)
    listings = Listing.objects.filter(owner=user).order_by('-created_at')
    consultations = ConsultationRequest.objects.filter(user=user)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'toggle_active':
            user.is_active = not user.is_active
            user.save()
            messages.success(request, 'وضعیت کاربر تغییر کرد.')
        elif action == 'toggle_staff':
            user.is_staff = not user.is_staff
            user.save()
            messages.success(request, 'دسترسی ادمین تغییر کرد.')
        elif action == 'toggle_verified':
            profile.is_verified = not profile.is_verified
            profile.save()
            messages.success(request, 'وضعیت تأیید تغییر کرد.')
        return redirect('panel_user_detail', pk=pk)

    return render(request, 'panel/user_detail.html', {
        'u': user, 'profile': profile,
        'listings': listings, 'consultations': consultations,
    })


@staff_member_required(login_url='/auth/login/')
def listings_list(request):
    q = request.GET.get('q', '')
    cat = request.GET.get('cat', '')
    status_filter = request.GET.get('status', '')
    listings = Listing.objects.select_related('owner').order_by('-created_at')
    if q:
        listings = listings.filter(title__icontains=q)
    if cat:
        listings = listings.filter(category=cat)
    if status_filter == 'active':
        listings = listings.filter(is_active=True)
    elif status_filter == 'inactive':
        listings = listings.filter(is_active=False)
    elif status_filter == 'featured':
        listings = listings.filter(is_featured=True)
    categories = CATEGORY_CHOICES
    return render(request, 'panel/listings.html', {
        'listings': listings, 'q': q, 'cat': cat,
        'status_filter': status_filter, 'categories': categories,
    })


@staff_member_required(login_url='/auth/login/')
def listing_toggle(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    action = request.POST.get('action')
    if action == 'toggle_active':
        listing.is_active = not listing.is_active
        listing.save()
    elif action == 'toggle_featured':
        listing.is_featured = not listing.is_featured
        listing.save()
    elif action == 'delete':
        listing.delete()
        messages.success(request, 'آگهی حذف شد.')
        return redirect('panel_listings')
    return redirect('panel_listings')


@staff_member_required(login_url='/auth/login/')
def categories_list(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            name = request.POST.get('name', '').strip()
            slug = request.POST.get('slug', '').strip()
            icon = request.POST.get('icon', '📦').strip()
            description = request.POST.get('description', '').strip()
            order = request.POST.get('order', 0)
            if name and slug:
                Category.objects.get_or_create(slug=slug, defaults={
                    'name': name, 'icon': icon,
                    'description': description, 'order': order,
                })
                messages.success(request, f'دسته‌بندی "{name}" اضافه شد.')
        elif action == 'delete':
            pk = request.POST.get('pk')
            Category.objects.filter(pk=pk).delete()
            messages.success(request, 'دسته‌بندی حذف شد.')
        elif action == 'toggle':
            pk = request.POST.get('pk')
            cat = get_object_or_404(Category, pk=pk)
            cat.is_active = not cat.is_active
            cat.save()
        return redirect('panel_categories')

    cats = Category.objects.all()
    return render(request, 'panel/categories.html', {'cats': cats})


@staff_member_required(login_url='/auth/login/')
def category_edit(request, pk):
    cat = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        cat.name = request.POST.get('name', cat.name).strip()
        cat.icon = request.POST.get('icon', cat.icon).strip()
        cat.description = request.POST.get('description', '').strip()
        cat.order = request.POST.get('order', cat.order)
        cat.save()
        messages.success(request, 'دسته‌بندی ویرایش شد.')
        return redirect('panel_categories')
    return render(request, 'panel/category_edit.html', {'cat': cat})


@staff_member_required(login_url='/auth/login/')
def visits_view(request):
    visits = SiteVisit.objects.order_by('-date')[:30]
    total_visits = sum(v.visits for v in SiteVisit.objects.all())
    total_unique = sum(v.unique_visits for v in SiteVisit.objects.all())
    today = timezone.now().date()
    today_v = SiteVisit.objects.filter(date=today).first()
    return render(request, 'panel/visits.html', {
        'visits': visits,
        'total_visits': total_visits,
        'total_unique': total_unique,
        'today_v': today_v,
    })


@staff_member_required(login_url='/auth/login/')
def consultations_view(request):
    status_filter = request.GET.get('status', '')
    items = ConsultationRequest.objects.select_related('user').order_by('-created_at')
    if status_filter:
        items = items.filter(status=status_filter)

    if request.method == 'POST':
        pk = request.POST.get('pk')
        new_status = request.POST.get('status')
        ConsultationRequest.objects.filter(pk=pk).update(status=new_status)
        messages.success(request, 'وضعیت درخواست تغییر کرد.')
        return redirect('panel_consultations')

    return render(request, 'panel/consultations.html', {
        'items': items, 'status_filter': status_filter,
    })
