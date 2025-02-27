from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True, blank=True)
    project_name = models.CharField(max_length=255, null=True)
    manager = models.ForeignKey("Manager", related_name="team", on_delete=models.SET_NULL, null=True)
    developers = models.ManyToManyField("Developer", related_name="+")
    created_by = models.ForeignKey("User", related_name='created_team', on_delete=models.SET_NULL, null=True, default=2)

    def __str__(self):
        return self.name    