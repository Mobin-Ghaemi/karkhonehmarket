from django.db import models
from django.contrib.auth.models import User


MEMBERSHIP_CHOICES = [
    ('free', 'رایگان'),
    ('gold', 'طلایی'),
    ('premium', 'ویژه'),
]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, verbose_name='تلفن')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='تصویر پروفایل')
    bio = models.TextField(blank=True, verbose_name='معرفی')
    company = models.CharField(max_length=200, blank=True, verbose_name='شرکت/سازمان')
    city = models.CharField(max_length=100, blank=True, verbose_name='شهر')
    membership = models.CharField(max_length=20, choices=MEMBERSHIP_CHOICES, default='free', verbose_name='نوع عضویت')
    membership_expires = models.DateTimeField(null=True, blank=True, verbose_name='انقضای عضویت')
    is_verified = models.BooleanField(default=False, verbose_name='تأیید شده')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'پروفایل کاربر'
        verbose_name_plural = 'پروفایل‌های کاربران'

    def __str__(self):
        return f'{self.user.get_full_name() or self.user.username}'

    def get_membership_label(self):
        return dict(MEMBERSHIP_CHOICES).get(self.membership, '')

    def listing_count(self):
        return self.user.listings.count()


CONSULTATION_STATUS = [
    ('pending', 'در انتظار بررسی'),
    ('contacted', 'تماس گرفته شد'),
    ('done', 'انجام شد'),
]

CONSULTATION_SUBJECT = [
    ('buy', 'خرید زمین / کارخانه'),
    ('sell', 'فروش زمین / کارخانه'),
    ('machinery', 'خرید یا فروش ماشین‌آلات'),
    ('import', 'واردات'),
    ('export', 'صادرات'),
    ('invest', 'سرمایه‌گذاری'),
    ('other', 'سایر'),
]


class ConsultationRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='consultations', verbose_name='کاربر')
    full_name = models.CharField(max_length=150, verbose_name='نام و نام خانوادگی')
    phone = models.CharField(max_length=20, verbose_name='شماره موبایل')
    subject = models.CharField(max_length=30, choices=CONSULTATION_SUBJECT, default='other', verbose_name='موضوع')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    status = models.CharField(max_length=20, choices=CONSULTATION_STATUS, default='pending', verbose_name='وضعیت')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'درخواست مشاوره'
        verbose_name_plural = 'درخواست‌های مشاوره'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.full_name} — {self.get_subject_display()}'
