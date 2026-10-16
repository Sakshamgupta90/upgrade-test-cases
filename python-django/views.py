import json

from django.http import HttpResponseBadRequest, JsonResponse
from django.utils import timezone
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods

NOTES = []


@require_http_methods(["GET", "POST"])
def notes(request):
    if request.method == "POST":
        if not request.is_ajax():
            return HttpResponseBadRequest(_("Expected an AJAX request"))
        data = json.loads(force_text(request.body))
        NOTES.append({
            "text": data["text"],
            "created": timezone.now().astimezone(timezone.utc).isoformat(),
        })
        return JsonResponse({"ok": True}, status=201)
    return JsonResponse({"notes": NOTES})


def note_detail(request, index):
    index = int(index)
    if index >= len(NOTES):
        return JsonResponse({"error": force_text(_("Not found"))}, status=404)
    return JsonResponse(NOTES[index])
