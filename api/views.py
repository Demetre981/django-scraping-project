from django.shortcuts import render

from api.forms import FindForm
from .models import Vacancy
# Create your views here.

def home_view(request):
    city = request.GET.get("city")
    proglanguage = request.GET.get("proglanguage")
    qs = []  # Default empty queryset
    form = FindForm()

    if city or proglanguage:
        _filter = {}
        if city:
            _filter["city__slug"] = city
        elif proglanguage:  # Changed `elif` to `if`
            _filter["programming_language__name"] = proglanguage

        qs = Vacancy.objects.filter(**_filter)
        
    return render(request, "home.html", {"object_list": qs, "form": form})