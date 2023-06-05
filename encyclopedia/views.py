from django.shortcuts import render

from . import util
from markdown2 import Markdown
from django.http import HttpResponseRedirect
from django.urls import reverse

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    markdownConverter = Markdown()

    contents = markdownConverter.convert(util.get_entry(title))
    return render(request, "encyclopedia/entry.html", {
        "contents": contents,
        "title": title
    })
