from django.db import models

class Manager(models.Model):
    full_name = models.CharField(max_length=255, null=False)
    experience = models.CharField(max_length=255, null=False)
    department = models.CharField(max_length=255, null=True)
    user = models.ForeignKey("User", related_name="manager", on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name
