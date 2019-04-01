from django.urls import path
from .views import *
urlpatterns = [
    path('', index),
    path('form/', feedback),
    path('stats/', stats)
]
