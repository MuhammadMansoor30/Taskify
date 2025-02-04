from django.db import models

class Task(models.Model):
    STATUS_CHOICES = [
        ('In Progress', 'In Progress'),
        ('Partially Completed', 'Partially Completed'),
        ('Completed', 'Completed'),
    ]

    SET_PRIORITY = [
        ('Low', "Low"),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    title = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True, blank=True)
    team = models.ForeignKey("Team", related_name="tasks", on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, default="In Progress")
    priority = models.CharField(choices=SET_PRIORITY, null=False)
    assigned_to = models.ForeignKey("User", related_name="tasks", on_delete=models.CASCADE)
    created_by = models.ManyToManyField("User", related_name="created_tasks")

    def save(self, *args, **kwargs):
        if not self.assigned_to and self.team:
            self.assigned_to = self.team.manager.user   # Gets the manager id from the user
        super(self).save(*args, **kwargs)

    def __str__(self):
        return self.title