from django.utils import timezone
from core.models import SiteVisit


class VisitTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if not any(path.startswith(p) for p in ['/admin/', '/myadmin/', '/static/', '/media/', '/favicon']):
            try:
                today = timezone.now().date()
                visit, _ = SiteVisit.objects.get_or_create(date=today)
                visit.visits += 1
                session_key = f'visited_{today}'
                if not request.session.get(session_key):
                    request.session[session_key] = True
                    visit.unique_visits += 1
                visit.save()
            except Exception:
                pass
        response = self.get_response(request)
        return response
