from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=255, null=False)
    code_name = models.CharField(max_length=255, null=False)
    created_at = models.TimeField(auto_now_add=True)
    permissions = models.ManyToManyField("Permission", related_name='roles')
    created_by = models.ForeignKey("User", related_name='user_roles', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
     