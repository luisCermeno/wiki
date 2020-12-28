from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.urls import reverse
from . import util
import random
import markdown2

class NewEntryForm(forms.Form):
  title = forms.CharField(label = "Title", 
          widget=forms.TextInput(attrs={'placeholder': 'Title here'})
          )
  content = forms.CharField(label = "Content", 
            widget=forms.Textarea(attrs={'placeholder': 'Write the content here using Mardown2 markup language.'})
            )

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if title in util.list_entries():
      return render(request, "encyclopedia/entry.html", {
          "title": title.capitalize(),
          "content": util.decode(title)
      })
    else:
      message = ('#Page not found\n'
          'We are **sorry** to announce that the page you are looking for has '
          'not been **created** yet.\n\n'
          'You might be the first creator to **write** it!'
      )
      return render(request, "encyclopedia/entry.html", {
          "title": "Page not found",
          "content": markdown2.markdown(message)
      })

def add(request):
  if request.method == "POST":
    # stores the data retrieved from the POST request into the object inputform
    inputform = NewEntryForm(request.POST)
    # if form is valid(server side validation)
    if inputform.is_valid():
      # takes the string in the attribute "task" and content from the object inputform 
      # and stores it in a variables called title and content 
      title = inputform.cleaned_data["title"]
      content = inputform.cleaned_data["content"]
      # write in file
      util.save_entry(title,content)
      return HttpResponseRedirect(reverse("encyclopedia:index"))
    # in case form is not valid, send back the form 
    else:
      return render(request, "encyclopedia/add.html", {
        "form": inputform
      })

  return render(request, "encyclopedia/add.html", {
    "form": NewEntryForm()
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