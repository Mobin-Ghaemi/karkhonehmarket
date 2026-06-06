from django.db import models
from django.contrib.auth.models import User


CATEGORY_CHOICES = [
    ('land', 'زمین صنعتی'),
    ('factory', 'کارخانه'),
    ('machinery', 'ماشین‌آلات'),
    ('import', 'واردات'),
    ('export', 'صادرات'),
    ('product', 'محصولات'),
]

STATUS_CHOICES = [
    ('sale', 'فروش'),
    ('rent', 'اجاره'),
    ('buy', 'خرید'),
]


class Listing(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name='دسته‌بندی')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='sale', verbose_name='نوع آگهی')
    description = models.TextField(verbose_name='توضیحات')
    price = models.BigIntegerField(null=True, blank=True, verbose_name='قیمت (تومان)')
    area = models.FloatField(null=True, blank=True, verbose_name='مساحت (متر مربع)')
    location = models.CharField(max_length=200, verbose_name='موقعیت')
    image = models.ImageField(upload_to='listings/', null=True, blank=True, verbose_name='تصویر')
    contact = models.CharField(max_length=50, verbose_name='تلفن تماس')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='listings', verbose_name='کاربر')
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False, verbose_name='ویژه')
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    class Meta:
        verbose_name = 'آگهی'
        verbose_name_plural = 'آگهی‌ها'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def formatted_price(self):
        if not self.price:
            return 'توافقی'
        p = self.price
        if p >= 1_000_000_000_000:
            val = p / 1_000_000_000_000
            return f"{val:,.0f} هزار میلیارد" if val == int(val) else f"{val:.1f} هزار میلیارد"
        if p >= 1_000_000_000:
            val = p / 1_000_000_000
            return f"{val:,.0f} میلیارد" if val == int(val) else f"{val:.1f} میلیارد"
        if p >= 1_000_000:
            val = p / 1_000_000
            return f"{val:,.0f} میلیون" if val == int(val) else f"{val:.1f} میلیون"
        return f"{p:,}"


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام دسته‌بندی')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='شناسه')
    icon = models.CharField(max_length=10, default='📦', verbose_name='آیکون')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    order = models.PositiveIntegerField(default=0, verbose_name='ترتیب نمایش')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def listing_count(self):
        return Listing.objects.filter(category=self.slug, is_active=True).count()


class SiteVisit(models.Model):
    date = models.DateField(unique=True)
    visits = models.PositiveIntegerField(default=0)
    unique_visits = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'بازدید سایت'
        verbose_name_plural = 'بازدیدهای سایت'
        ordering = ['-date']

    def __str__(self):
        return str(self.date)
