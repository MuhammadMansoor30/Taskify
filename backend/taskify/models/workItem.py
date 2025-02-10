from django.db import models

class WorkItem(models.Model):
    STATUS_CHOICES = [
        ('In Progress', 'In Progress'),
        ('Partially Completed', 'Partially Completed'),
        ('Completed', 'Completed'),
    ]

    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='work_files')
    status = models.CharField(choices=STATUS_CHOICES, default="In Progress")
    is_approved = models.BooleanField(default=False)
    task = models.ForeignKey("Task", related_name='work', on_delete=models.SET_NULL, null=True)
    added_by = models.ForeignKey("User", related_name='workItem', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name