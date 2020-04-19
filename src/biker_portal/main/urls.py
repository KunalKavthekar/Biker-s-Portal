from django.urls import path
from . import views

urlpatterns = [
path("<int:id>", views.index, name="index"),
path("home/", views.home, name="home"),
# path("", views.login, name="login"),
path("create/", views.create, name="create"),
path("view/", views.view, name="view"),
path("about/", views.about, name="about"),
path("getlocation/", views.getLocation,name="getlocation"),
# path("getdistance/", views.getDistance,name="getdistance"),
path("new_search/", views.new_search, name="new_search"),
path("getWeather/", views.getWeather, name="getWeather"),
]