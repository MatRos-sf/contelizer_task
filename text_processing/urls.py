from django.urls import path

from . import views

urlpatterns = [
    path("", views.TextProcessingFormView.as_view(), name="text_processing"),
    path("results/<str:filename>", views.ResultsView.as_view(), name="results"),
]
