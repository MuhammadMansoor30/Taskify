import os
import django

# Setting up Django and Setting file and then importing models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')  
django.setup()

from taskify.models import User, Permission, Role

permissions = [
    {"name": "Create User", "code_name": "user_create", "description": "Can Create a User"},
    {"name": "Add Manager", "code_name": "manager_add", "description": "Can Add a Manager"},
    {"name": "Add Developer", "code_name": "developer_add", "description": "Can Add a Developer"},
    {"name": "Add Team", "code_name": "team_add", "description": "Can Add a new Team"},
    {"name": "Add Task", "code_name": "task_add", "description": "Can Add a new Task"},
    {"name": "Publish Work", "code_name": "work_publish", "description": "Can Publish their work"},
    {"name": "Approve Work", "code_name": "approve_work", "description": "Can Approve a Work"},
    {"name": "Update User", "code_name": "user_update", "description": "Can Update a User"},
    {"name": "Delete User", "code_name": "user_delete", "description": "Can Delete a User"},
    {"name": "Edit Manager", "code_name": "manager_edit", "description": "Can Edit a Manager"},
    {"name": "Delete Manager", "code_name": "manager_delete", "description": "Can Delete a Manager"},
    {"name": "Edit Developer", "code_name": "developer_edit", "description": "Can Edit a Developer"},
    {"name": "Delete Developer", "code_name": "developer_delete", "description": "Can Delete a Developer"},
    {"name": "Edit Team", "code_name": "team_edit", "description": "Can Edit a Team"},
    {"name": "Delete Team", "code_name": "team_delete", "description": "Can Delete a Team"},
    {"name": "Edit Task", "code_name": "task_edit", "description": "Can Edit a Task"},
    {"name": "Delete Task", "code_name": "task_delete", "description": "Can Delete a Task"},
    {"name": "Delete Work", "code_name": "work_delete", "description": "Can Delete their published work"},
    {"name": "Add Role", "code_name": "role_add", "description": "Can Add a new Role"},
    {"name": "Get Roles", "code_name": "roles_get", "description": "Can Get all Role"},
    {"name": "Get Permissions", "code_name": "permissions_get", "description": "Can Get all Permissions"},
]

def add_permissions_and_admin_role():
    for perm_list in permissions:
        try:
            Permission.objects.get(code_name=perm_list['code_name'])
        except Permission.DoesNotExist:
            Permission.objects.create(
                name = perm_list['name'],
                code_name = perm_list['code_name'],
                description = perm_list['description']
            )    
    
    all_perm = Permission.objects.all()
    try:
        Role.objects.get(code_name='adm')
    except Role.DoesNotExist:
        role = Role.objects.create(name = "Admin", code_name = "adm")
        role.permissions.clear()
        role.permissions.add(*all_perm)
        role.save()


def createSuperUser():
    user = User.objects.create_superuser(
        username = "admin",
        email = "admin@email.com",
        password = 'abcd@1234',
        cnic = '9821489654752',
        mobile_no = '03216975324'
    )

    role = Role.objects.get(code_name='adm')

    user.roles.clear()
    user.roles.add(role)
    user.save()

    print(user)
    return user 

if __name__ == "__main__":
    print("Adding Permissions and Admin Role")
    add_permissions_and_admin_role()

    try:
        User.objects.get(email='admin@email.com', is_staff=True)
    except User.DoesNotExist:
        print("Creating and adding superUser")
        createSuperUser()
    