from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:title>', views.entry, name="entry"),
    path('add', views.add, name="add"),
    path('search', views.search, name="search"),
    path('random', views.render_random, name="random"),
]