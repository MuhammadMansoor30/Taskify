from django.urls import path
from taskify import views

urlpatterns = [
    path('login/', view=views.LoginView.as_view()),
    path('logout/', view=views.LogoutView.as_view()),
    path('permissions/', view=views.PermissionListView.as_view()),
    path('roles/', view=views.RoleListCreateView.as_view()),
    path('managers/', view=views.ManagerListCreateView.as_view()),
    path('managers/<int:pk>/update/', view=views.ManagerUpdateDestroyView.as_view()),
    path('managers/<int:pk>/delete/', view=views.ManagerUpdateDestroyView.as_view()),
    path('teams/', view=views.TeamListCreateView.as_view()),
    path('teams/<int:pk>/update/', view=views.TeamUpdateDestroyView.as_view()),
    path('teams/<int:pk>/delete/', view=views.TeamUpdateDestroyView.as_view()),
    path('developers/', view=views.DeveloperListCreateView.as_view()),
    path('developers/<int:pk>/update/', view=views.DeveloperUpdateDestroyView.as_view()),
    path('developers/<int:pk>/delete/', view=views.DeveloperUpdateDestroyView.as_view()),
    path('tasks/', view=views.TaskListCreateView.as_view()),
    path('tasks/<int:pk>/update/', view=views.TaskUpdateDestroyView.as_view()),
    path('tasks/<int:pk>/delete/', view=views.TaskUpdateDestroyView.as_view()),
    path('workItems/', view=views.WorkItemListCreateView.as_view()),
    path('workItems/<int:pk>/update/', view=views.WorkItemUpdateDestroyView.as_view()),
    path('workItems/<int:pk>/delete/', view=views.WorkItemUpdateDestroyView.as_view()),
    path('workItems/<int:pk>/approve/', view=views.WorkItemApproveView.as_view()),
]