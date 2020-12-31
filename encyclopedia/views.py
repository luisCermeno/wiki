import random, markdown2

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.urls import reverse

from . import util


class NewEntryForm(forms.Form):
    title = forms.CharField(
        label = "Title", 
        widget = forms.TextInput(attrs={
            'placeholder': 'Title here'
        })
    )
    content = forms.CharField(
        label = "Content", 
        widget = forms.Textarea(attrs={
            'placeholder': 'Write the content here using Mardown2 markup language.'
        })
    )

msg_notfound = ('#Page not found\n'
    'We are **sorry** to announce that the page you are looking for has '
    'not been **created** yet.\n\n'
    'You might be the first creator to **write** it!'
)

msg_aldycreated = ('#####The page you just submitted already exists!\n'
    'A page with the **same title** already exists in the wiki.\n\n'
    '**Check it out** searching for it or try again.'
)

msg_invalidform = ('#####Sorry, it looks like there is something wrong!\n'
    'We could not add you page because the **title** or **content** you just submitted is **not valid**.\n\n '
    'Please **try again**.'
)


def index(request):
        return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries()
        })


def entry(request, title):
    if 'edit' in request.GET:
        editform = NewEntryForm(
            initial={
                'title': title, 
                'content': util.get_entry(title)
            })
        return render(request, "encyclopedia/add.html", {
            "edit" : request.GET["edit"],
            "title": title,
            "form": editform
        })
    else:
        if title in util.list_entries():
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": util.decode(title)
            })
        else:
            return render(request, "encyclopedia/entry.html", {
                "title": "Page not found",
                "content": markdown2.markdown(msg_notfound)
            })


def add(request):
    if request.method == "POST":
        # stores the data retrieved from the POST request into the object inputform
        inputform = NewEntryForm(request.POST)
        edit = request.POST["edit"]
        # if form is valid(server side validation)
        if inputform.is_valid():
            # takes the string in the attribute "task" and content from the object inputform 
            # and stores it in a variables called title and content 
            title = inputform.cleaned_data["title"]
            content = inputform.cleaned_data["content"]
            # check if there is the entry is repeated and store it in variable
            repeated = (title.upper() in [x.upper() for x in util.list_entries()])
            # write in file
            if edit == "true" or not repeated:
                util.save_entry(title,content)
                return render(request, "encyclopedia/entry.html", {
                  "title": title,
                  "content": util.decode(title)
                })
            else:
                return render(request, "encyclopedia/add.html", {
                    "edit": edit,
                    "form": inputform,
                    "msg": markdown2.markdown(msg_aldycreated)
                })
        # in case form is not valid, send back the form 
        else:
            return render(request, "encyclopedia/add.html", {
                "edit": edit,
                "form": inputform,
                "msg": markdown2.markdown(msg_invalidform)
            })
    elif request.method == "GET":
        return render(request, "encyclopedia/add.html", {
                "edit": "false",
                "form": NewEntryForm(),
        })


def search(request):
    if request.method == "GET":
        target = request.GET['q']
        for entry in util.list_entries():
            if target.upper() == entry.upper():
                return redirect('encyclopedia:entry', title=entry)
        else:
            return render(request, "encyclopedia/search.html", {
                "results": util.match(target),
                "title": target
        })


def render_random(request):
    random_title = random.choice(util.list_entries())
    return redirect('encyclopedia:entry', title=random_title)