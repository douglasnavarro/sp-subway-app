from django.urls import path
from .views import ReadingsListView

urlpatterns = [
    path('', ReadingsListView.as_view()),
]