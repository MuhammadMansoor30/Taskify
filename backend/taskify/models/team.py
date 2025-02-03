from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True, blank=True)
    project_assigned = models.CharField(max_length=255, null=True)
    manager = models.OneToOneField("Manager", related_name="team", on_delete=models.CASCADE)

    def __str__(self):
        return self.name