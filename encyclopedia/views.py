import random
from django.shortcuts import render
from markdown2 import Markdown
from django.http import HttpResponseRedirect
from django import forms
from . import util


markdowner = Markdown()  # Markdown object for markdown-to-html conversion


def index(request):
    """
    Rendering index.html with a list of all article entries
    """
    return render(
        request,
        "encyclopedia/index.html",
        {"entries": util.list_entries(), "search_form": SearchForm()},
    )


def entry(request, title):
    """
    Looping over the entry list, rendering a wiki arcticle html converted from its markdown file. For non-existing markdown
    files / entries redicrect to the notfound error page.
    """
    entries = util.list_entries()
    for entry in entries:
        if title.lower() == entry.lower():
            return render(
                request,
                "encyclopedia/entry.html",
                {"title": title, "content": markdowner.convert(util.get_entry(title)),
                "search_form": SearchForm()}
            )
    return HttpResponseRedirect("/notfound")


def not_found(request):
    """
    Rendering the error page for a non-existing article
    """
    return render(request, "encyclopedia/notfound.html", {"search_form": SearchForm()})


def randompage(request):
    """
    Redirecting to a random article
    """
    randomized = random.choice(util.list_entries())
    return HttpResponseRedirect(f"wiki/{randomized}")


class EntryForm(forms.Form):
    """
    Form to add a new entry
    """

    title = forms.CharField(label="Title", required=True)
    body = forms.CharField(widget=forms.Textarea(), label="Content", required=True)


def create_page(request):
    """
    Rendering the "add new page"-html. When the form gets submitted the user is submitted to the newly created
    entry page. If the entry already exists, the user is redirected to the "already existing"-error page.
    """
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            body = form.cleaned_data["body"]
            if util.get_entry(title) == None:
                util.save_entry(title, body)
                return HttpResponseRedirect(f"wiki/{title}")
            else:
                return HttpResponseRedirect("/existing")
    else:
        return render(request, "encyclopedia/newpage.html", {"entry_form": EntryForm(),
        "search_form": SearchForm()})


def existing_page(request):
    return render(request, "encyclopedia/existing.html")


class EditForm(forms.Form):
    body = forms.CharField(label="Content", required=True, widget=forms.Textarea())


def edit(request, title):
    if request.method == "GET":
        body = util.get_entry(title)
        return render(
            request,
            "encyclopedia/editpage.html",
            {"title": title, "edit_form": EditForm(initial={"body": body})},
        )

    elif request.method == "POST":
        form = EditForm(request.POST)

        if form.is_valid():
            body = form.cleaned_data["body"]
            util.save_entry(title, body)
            return HttpResponseRedirect(f"../wiki/{title}")


def no_results(request):
    return render(request, "encyclopedia/no_results.html")


class SearchForm(forms.Form):
    search = forms.CharField()


def search(request):
    if request.method == "GET":
        form = SearchForm(request.GET)

        if form.is_valid():
            query = form.cleaned_data["search"]
            entries = util.list_entries()
            results = [entry for entry in entries if query.lower() in entry.lower()]
            
            if len(results) == 0:
                return HttpResponseRedirect("/no_results")
            elif len(results) == 1:
                return HttpResponseRedirect(f"wiki/{results[0]}")
            else:
                return render(
                    request, "encyclopedia/results.html", {"results": results}
                )
