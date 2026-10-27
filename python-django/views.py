import datetime
import json

from django.http import HttpResponseBadRequest, JsonResponse
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods

NOTES = []


@require_http_methods(["GET", "POST"])
def notes(request):
    if request.method == "POST":
        if request.headers.get("X-Requested-With") != "XMLHttpRequest":
            return HttpResponseBadRequest(force_str(_("Expected an AJAX request")))
        data = json.loads(force_str(request.body))
        NOTES.append({
            "text": data["text"],
            "created": timezone.now().astimezone(datetime.timezone.utc).isoformat(),
        })
        return JsonResponse({"ok": True}, status=201)
    return JsonResponse({"notes": NOTES})


def note_detail(request, index):
    index = int(index)
    if index >= len(NOTES):
        return JsonResponse({"error": force_str(_("Not found"))}, status=404)
    return JsonResponse(NOTES[index])
