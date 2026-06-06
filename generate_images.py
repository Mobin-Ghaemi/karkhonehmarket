import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Listing

svgs = {
    'land': {
        'bg': '#EFF6FF', 'accent': '#1E6BB8', 'icon': '''
        <rect x="200" y="280" width="400" height="8" rx="4" fill="#1E6BB8" opacity="0.3"/>
        <rect x="160" y="220" width="480" height="60" rx="6" fill="#1E6BB8" opacity="0.12"/>
        <rect x="240" y="150" width="120" height="70" rx="6" fill="#2081E2" opacity="0.2"/>
        <rect x="380" y="120" width="160" height="100" rx="6" fill="#2081E2" opacity="0.25"/>
        <circle cx="400" cy="180" r="16" fill="#2081E2" opacity="0.5"/>
        <line x1="390" y1="196" x2="390" y2="220" stroke="#2081E2" stroke-width="3" opacity="0.4"/>
        <line x1="410" y1="196" x2="410" y2="220" stroke="#2081E2" stroke-width="3" opacity="0.4"/>
        <text x="400" y="340" text-anchor="middle" font-family="Arial" font-size="22" font-weight="bold" fill="#1E6BB8" opacity="0.7">زمین صنعتی</text>
        ''',
    },
    'factory': {
        'bg': '#F0F9FF', 'accent': '#0369A1', 'icon': '''
        <rect x="180" y="230" width="440" height="80" rx="4" fill="#0369A1" opacity="0.15"/>
        <rect x="200" y="170" width="80" height="60" rx="4" fill="#0369A1" opacity="0.2"/>
        <rect x="310" y="150" width="100" height="80" rx="4" fill="#0369A1" opacity="0.25"/>
        <rect x="440" y="180" width="80" height="50" rx="4" fill="#0369A1" opacity="0.2"/>
        <rect x="220" y="130" width="20" height="40" rx="3" fill="#0369A1" opacity="0.3"/>
        <rect x="250" y="140" width="20" height="30" rx="3" fill="#0369A1" opacity="0.3"/>
        <rect x="330" y="110" width="20" height="40" rx="3" fill="#0369A1" opacity="0.35"/>
        <rect x="360" y="120" width="20" height="30" rx="3" fill="#0369A1" opacity="0.3"/>
        <rect x="180" y="305" width="440" height="10" rx="3" fill="#0369A1" opacity="0.2"/>
        <text x="400" y="355" text-anchor="middle" font-family="Arial" font-size="22" font-weight="bold" fill="#0369A1" opacity="0.7">کارخانه</text>
        ''',
    },
    'machinery': {
        'bg': '#F5F3FF', 'accent': '#5B21B6', 'icon': '''
        <circle cx="400" cy="220" r="70" fill="none" stroke="#5B21B6" stroke-width="12" opacity="0.2"/>
        <circle cx="400" cy="220" r="45" fill="none" stroke="#5B21B6" stroke-width="8" opacity="0.25"/>
        <circle cx="400" cy="220" r="20" fill="#5B21B6" opacity="0.3"/>
        <rect x="388" y="148" width="24" height="30" rx="4" fill="#5B21B6" opacity="0.25"/>
        <rect x="388" y="262" width="24" height="30" rx="4" fill="#5B21B6" opacity="0.25"/>
        <rect x="298" y="208" width="30" height="24" rx="4" fill="#5B21B6" opacity="0.25"/>
        <rect x="472" y="208" width="30" height="24" rx="4" fill="#5B21B6" opacity="0.25"/>
        <text x="400" y="340" text-anchor="middle" font-family="Arial" font-size="22" font-weight="bold" fill="#5B21B6" opacity="0.7">ماشین‌آلات</text>
        ''',
    },
    'import': {
        'bg': '#ECFDF5', 'accent': '#065F46', 'icon': '''
        <rect x="230" y="200" width="340" height="100" rx="8" fill="#065F46" opacity="0.12"/>
        <rect x="250" y="220" width="60" height="60" rx="4" fill="#065F46" opacity="0.2"/>
        <rect x="325" y="220" width="60" height="60" rx="4" fill="#065F46" opacity="0.2"/>
        <rect x="400" y="220" width="60" height="60" rx="4" fill="#065F46" opacity="0.2"/>
        <rect x="475" y="220" width="60" height="60" rx="4" fill="#065F46" opacity="0.2"/>
        <polygon points="320,170 480,170 510,200 290,200" fill="#065F46" opacity="0.15"/>
        <line x1="400" y1="150" x2="400" y2="200" stroke="#065F46" stroke-width="3" opacity="0.3"/>
        <polygon points="390,140 410,140 400,155" fill="#065F46" opacity="0.4"/>
        <text x="400" y="345" text-anchor="middle" font-family="Arial" font-size="22" font-weight="bold" fill="#065F46" opacity="0.7">واردات</text>
        ''',
    },
    'export': {
        'bg': '#FFF7ED', 'accent': '#9A3412', 'icon': '''
        <ellipse cx="400" cy="260" rx="180" ry="30" fill="#9A3412" opacity="0.1"/>
        <polygon points="310,240 490,240 520,260 280,260" fill="#9A3412" opacity="0.15"/>
        <rect x="350" y="200" width="100" height="40" rx="6" fill="#9A3412" opacity="0.18"/>
        <polygon points="280,260 310,160 490,160 520,260" fill="#9A3412" opacity="0.1"/>
        <rect x="370" y="160" width="60" height="40" rx="4" fill="#9A3412" opacity="0.2"/>
        <line x1="400" y1="120" x2="400" y2="160" stroke="#9A3412" stroke-width="2" opacity="0.3"/>
        <rect x="390" y="100" width="40" height="25" rx="2" fill="#9A3412" opacity="0.2"/>
        <text x="400" y="320" text-anchor="middle" font-family="Arial" font-size="22" font-weight="bold" fill="#9A3412" opacity="0.7">صادرات</text>
        ''',
    },
}

for listing in Listing.objects.all():
    cat = listing.category
    style = svgs.get(cat, svgs['land'])
    idx = listing.pk

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="400" viewBox="0 0 800 400">
  <defs>
    <linearGradient id="bg{idx}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{style['bg']};stop-opacity:1"/>
      <stop offset="100%" style="stop-color:{style['bg']};stop-opacity:0.6"/>
    </linearGradient>
    <pattern id="dots{idx}" x="0" y="0" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="12" cy="12" r="1.5" fill="{style['accent']}" opacity="0.15"/>
    </pattern>
  </defs>
  <rect width="800" height="400" fill="url(#bg{idx})"/>
  <rect width="800" height="400" fill="url(#dots{idx})"/>
  {style['icon']}
</svg>'''

    filename = f'listings/listing_{idx}.svg'
    filepath = f'media/{filename}'
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(svg)

    listing.image = filename
    listing.save()
    print(f'✓ {listing.title[:30]} → {filename}')

print('\nDone!')
