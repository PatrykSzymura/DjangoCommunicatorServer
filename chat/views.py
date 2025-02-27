from django.shortcuts import render
from django.template.loader import render_to_string

# Create your views here.
from django.http import HttpResponse



def index(request):
    rendered = render_to_string("sus.html")
    return HttpResponse(rendered)