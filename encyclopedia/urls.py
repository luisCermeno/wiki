from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path('entries/<str:title>', views.entry, name="entry"),
    path('add', views.add, name="add")
]
