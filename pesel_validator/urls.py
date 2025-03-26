from django.urls import path

from .views import PeselView

urlpatterns = [
    path("", PeselView.as_view(), name="pesel"),
]
