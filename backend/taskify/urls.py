from django.urls import path
from taskify import views

urlpatterns = [
    path('login/', view=views.LoginView.as_view()),
    path('permissions/', view=views.PermissionListView.as_view()),
    path('roles/', view=views.RoleListCreateView.as_view()),
    path('managers/', view=views.ManagerListCreateView.as_view()),
    path('managers/<int:pk>/update/', view=views.ManagerUpdateDestroyView.as_view()),
    path('managers/<int:pk>/delete/', view=views.ManagerUpdateDestroyView.as_view()),
    path('teams/', view=views.TeamListCreateView.as_view()),
    path('teams/<int:pk>/update/', view=views.TeamUpdateDestroyView.as_view()),
    path('teams/<int:pk>/delete/', view=views.TeamUpdateDestroyView.as_view()),
]