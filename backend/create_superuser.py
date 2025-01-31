import os
import django

# Setting up Django and Setting file and then importing models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')  
django.setup()

from taskify.models.user import User


def createSuperUser():
    user = User.objects.create_superuser(
        username = "admin",
        email = "admin@email.com",
        password = 'abcd@1234',
        cnic = '9821489654752',
        mobile_no = '03216975324'
    )

    user.save()

    print(user)
    return user

createSuperUser()