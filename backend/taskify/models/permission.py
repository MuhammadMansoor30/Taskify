from django.db import models

class Permission(models.Model):
    name = models.CharField(max_length=255, null=False)
    code_name = models.CharField(max_length=255, null=False)
    description = models.TextField()
    created_at = models.TimeField(auto_now=True)