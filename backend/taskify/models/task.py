from django.db import models

class Task(models.Model):
    # STATUS_CHOICES = [
    #     ('In Progress', 'In Progress'),
    #     ('Partially Completed', 'Partially Completed'),
    #     ('Completed', 'Completed'),
    # ]

    SET_PRIORITY = [
        ('Low', "Low"),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    title = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True, blank=True)
    team = models.ForeignKey("Team", related_name="tasks", on_delete=models.SET_NULL, null=True)
    # status = models.CharField(choices=STATUS_CHOICES, default="In Progress")
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(choices=SET_PRIORITY, null=False)
    assigned_to = models.ForeignKey("User", related_name="tasks", on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey("User", related_name="created_tasks", on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        if not self.assigned_to and self.team:
            self.assigned_to = self.team.manager.user   # Gets the manager id from the user
        super(Task, self).save(*args, **kwargs)       # We have use to use the Type/Model name as first Arg or else it will throw positional arg error

    def __str__(self):
        return self.title