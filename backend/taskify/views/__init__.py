from .login_view import LoginView
from .permission_list_view import PermissionListView
from .role_list_create_view import RoleListCreateView

# By adding import here in the '__init__.py' file we can simply import it in the views using: from <appname>.views import <ViewName>
# We dont have to refer to py file then. Same is the case for models and serializers as well. We can use this syntax or dont use it as per our choice.