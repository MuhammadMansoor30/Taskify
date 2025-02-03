from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, username, email, password, cnic, mobile_no):
        if not email and not username and not cnic:
            raise ValueError("Email, Username and CNIC must be provided")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            cnic = cnic,
            mobile_no = mobile_no
        )

        user.set_password(password)
        user.save(using = self._db)
        
        return user
    
    def create_superuser(self, username, email, password, cnic, mobile_no):
        user = self.create_user(username, email, password, cnic, mobile_no)
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        
        return user

# To create a user or superuser either create a script file to create users or use python shell

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=250, null=False)
    email = models.EmailField(max_length=250, unique=True)
    password = models.CharField(max_length=250, null=False)
    roles = models.ManyToManyField("Role", related_name="users")
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    cnic = models.CharField(max_length=250, null=False)
    mobile_no = models.CharField(max_length=150, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    objects = UserManager()

    def __str__(self):
        return self.email
    
    # Have to add role to it after adding the Role and Permission Models.