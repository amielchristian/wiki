from django.shortcuts import render

from . import util
from markdown2 import Markdown
from django.http import HttpResponseRedirect
from django.urls import reverse

entries = util.list_entries()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    markdownConverter = Markdown()

    try:
        markdown = util.get_entry(title)
        if markdown != None:
            contents = markdownConverter.convert(markdown)
            return render(request, "encyclopedia/entry.html", {
                "contents": contents,
                "title": title
            })
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        return render(request, "encyclopedia/error.html", {
            "error_code": 1
        })

def search(request):
    query = request.GET.get("query")
    
    # make all entries lowercase to make the search case-insensitive
    entries_lc = []
    for i in range(len(entries)):
        entries_lc.append(entries[i].lower())

    # if the query matches an entry perfectly (letter cases notwithstanding), redirect to that entry's page
    if query.lower() in entries_lc:
        i = entries_lc.index(query.lower())
        return HttpResponseRedirect(reverse("entry", args=[entries[i]]))
    # display entries that include the query as a substring if nothing matches perfectly
    else:
        candidates = []
        for entry in entries_lc:
            # if a string contains a substring (this search is also case-insensitive), then append to the list of candidate entries
            if query.lower() in entry:
                i = entries_lc.index(entry)
                candidates.append(entries[i])

        return render(request, "encyclopedia/search.html", {
            "results": candidates,
            "query": query
        })
    
def create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        # create file
        try:
            f = open("entries/"+title+".md", "x")
            f.write(content)
            f.close()

            return HttpResponseRedirect(reverse("entry", args=[title]))
        except FileExistsError:
            return render(request, "encyclopedia/error.html", {
            "error_code": 2,
            "title": title
        })

    return render(request, "encyclopedia/create.html")

