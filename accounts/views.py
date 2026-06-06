from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count
from .models import UserProfile, ConsultationRequest, CONSULTATION_SUBJECT
from .forms import RegisterForm, LoginForm, ProfileForm
from core.models import Listing, CATEGORY_CHOICES


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        cd = form.cleaned_data
        user = User.objects.create_user(
            username=cd['username'],
            email=cd['email'],
            password=cd['password'],
            first_name=cd['first_name'],
            last_name=cd['last_name'],
        )
        UserProfile.objects.create(user=user, phone=cd['phone'])
        login(request, user)
        messages.success(request, f'خوش آمدید {user.first_name}! حساب شما با موفقیت ایجاد شد.')
        return redirect('dashboard')
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request.POST or None)
    error = None
    if request.method == 'POST' and form.is_valid():
        cd = form.cleaned_data
        user = authenticate(request, username=cd['username'], password=cd['password'])
        if user is None:
            # try by email
            try:
                u = User.objects.get(email=cd['username'])
                user = authenticate(request, username=u.username, password=cd['password'])
            except User.DoesNotExist:
                pass
        if user:
            login(request, user)
            if not cd.get('remember'):
                request.session.set_expiry(0)
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            error = 'نام کاربری یا رمز عبور اشتباه است.'
    return render(request, 'accounts/login.html', {'form': form, 'error': error})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    my_listings = Listing.objects.filter(owner=request.user)
    stats = {
        'total': my_listings.count(),
        'active': my_listings.filter(is_active=True).count(),
        'featured': my_listings.filter(is_featured=True).count(),
        'sale': my_listings.filter(status='sale').count(),
    }
    recent = my_listings.order_by('-created_at')[:5]
    return render(request, 'accounts/dashboard.html', {
        'profile': profile,
        'stats': stats,
        'recent': recent,
    })


@login_required
def my_listings(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    listings = Listing.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'accounts/my_listings.html', {
        'profile': profile,
        'listings': listings,
    })


@login_required
def edit_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.user, request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            request.user.first_name = form.cleaned_data.get('first_name', '')
            request.user.last_name = form.cleaned_data.get('last_name', '')
            request.user.email = form.cleaned_data.get('email', '')
            request.user.save()
            messages.success(request, 'پروفایل با موفقیت بروزرسانی شد.')
            return redirect('edit_profile')
    else:
        form = ProfileForm(request.user, instance=profile)
    return render(request, 'accounts/edit_profile.html', {'form': form, 'profile': profile})


@login_required
def post_listing(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        d = request.POST
        listing = Listing(
            title=d.get('title', ''),
            category=d.get('category', 'land'),
            status=d.get('status', 'sale'),
            description=d.get('description', ''),
            location=d.get('location', ''),
            contact=d.get('contact', request.user.profile.phone or ''),
            owner=request.user,
        )
        try:
            listing.price = int(d.get('price', '0').replace(',', '')) or None
        except:
            listing.price = None
        try:
            listing.area = float(d.get('area', '0')) or None
        except:
            listing.area = None
        if 'image' in request.FILES:
            listing.image = request.FILES['image']
        listing.save()
        messages.success(request, 'آگهی شما با موفقیت ثبت شد.')
        return redirect('my_listings')
    return render(request, 'accounts/post_listing.html', {
        'profile': profile,
        'categories': CATEGORY_CHOICES,
    })


@login_required
def delete_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk, owner=request.user)
    if request.method == 'POST':
        listing.delete()
        messages.success(request, 'آگهی حذف شد.')
    return redirect('my_listings')


@login_required
def consultation(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    my_requests = ConsultationRequest.objects.filter(user=request.user)
    error = None

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', 'other')
        description = request.POST.get('description', '').strip()

        if not full_name or not phone:
            error = 'نام و شماره موبایل الزامی است.'
        else:
            ConsultationRequest.objects.create(
                user=request.user,
                full_name=full_name,
                phone=phone,
                subject=subject,
                description=description,
            )
            messages.success(request, 'درخواست مشاوره شما ثبت شد. به زودی با شما تماس می‌گیریم.')
            return redirect('consultation')

    return render(request, 'accounts/consultation.html', {
        'profile': profile,
        'my_requests': my_requests,
        'subjects': CONSULTATION_SUBJECT,
        'error': error,
    })

