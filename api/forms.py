from django import forms
from api.models import City, ProgLanguage

class FindForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(), 
                                  to_field_name="slug", required=False,
                                  widget=forms.Select(attrs={"class": "form-control"}), label="City")
    proglanguage = forms.ModelChoiceField(queryset=ProgLanguage.objects.all(), 
                                          to_field_name="name", required=False,
                                          widget=forms.Select(attrs={"class": "form-control"}), label="Programming language")