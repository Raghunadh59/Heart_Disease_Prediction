from django.urls import path
from . import views

urlpatterns = [
    path("" , views.home , name = "index"),
    path("predict" , views.predict, name = "predict"),
    path("submit" , views.submit, name = "submit")
]
#