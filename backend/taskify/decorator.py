from django.core.exceptions import PermissionDenied

def permission_required(perm):
    def inner(function):
        def wrapper(self, *args, **kwargs):
            perm_lst = [] 
            # Checking for permissions inside of user and roles and getting them
            for role in self.request.user.roles.all():
                role_perm = role.permissions.all()
                for permission in role_perm:
                    perm_lst.append(permission.code_name)
            # Checking for permissions inside of permisison passed from view
            for p in perm:
                has_perm = p in perm_lst
                if has_perm:
                    return function(self, *args, **kwargs)
            raise PermissionDenied
        return wrapper
    return inner
