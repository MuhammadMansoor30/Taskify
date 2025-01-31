from django.urls import path
from taskify import views

urlpatterns = [
    path('login/', view=views.LoginView.as_view()),
]