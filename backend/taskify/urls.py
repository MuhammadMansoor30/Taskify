from django.urls import path
from taskify import views

urlpatterns = [
    path('login/', view=views.LoginView.as_view()),
    path('permissions/', view=views.PermissionListView.as_view()),
    path('roles/', view=views.RoleListCreateView.as_view()),
]