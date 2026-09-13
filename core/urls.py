from django.urls import include, path
from core import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path("duckies/", include("duckies.urls")),
]