from django.db import models

class Developer(models.Model):
    full_name = models.CharField(max_length=255, null=False)
    experience = models.CharField(max_length=255, null=False)
    skill_set = models.CharField(max_length=255, null=True)
    user = models.ForeignKey("User", related_name="developer", on_delete=models.CASCADE)
    manager = models.ForeignKey("Manager", related_name="developers", on_delete=models.SET_NULL, null=True)
    team = models.ForeignKey("Team", related_name="+", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.full_name