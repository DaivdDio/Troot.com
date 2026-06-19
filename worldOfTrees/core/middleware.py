# core/middleware.py

from .models import SiteStats
from django.db.models import F

class VisitCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if not request.session.get("has_visited"):

            stats, _ = SiteStats.objects.get_or_create(pk=1)

            SiteStats.objects.filter(pk=1).update(
                total_visits=F("total_visits") + 1
            )

            request.session["has_visited"] = True

        return self.get_response(request)