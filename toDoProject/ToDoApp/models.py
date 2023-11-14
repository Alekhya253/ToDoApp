
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    finish_by = models.DateTimeField()
    is_finished = models.BooleanField(default=False)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    collaborators = models.ManyToManyField(User, related_name='collaborators', blank=True)
    attachments = models.ManyToManyField('Attachment', related_name='attachments', blank=True)

    def get_absolute_url(self):
        return reverse("task-detail", args=[str(self.id)])

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['created_at']

class Attachment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    file = models.FileField(upload_to='media/task_attachments/')
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Attachment for Task: {self.task.title}"
