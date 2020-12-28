from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse
from . import util

class NewEntryForm(forms.Form):
  form_title = forms.CharField(label = "Title")
  form_content = forms.CharField(label = "Content")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    return render(request, "encyclopedia/entry.html", {
        "title": title.capitalize(),
        "content": util.decode(title)
    })

def add(request):
  if request.method == "POST":
    # stores the data retrieved from the POST request into the object inputform
    inputform = NewEntryForm(request.POST)
    # if form is valid(server side validation)
    if inputform.is_valid():
      # takes the string in the attribute "task" and content from the object inputform 
      # and stores it in a variables called title and content 
      title = inputform.cleaned_data["form_title"]
      content = inputform.cleaned_data["form_content"]
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