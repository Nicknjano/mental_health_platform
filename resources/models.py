from django.db import models

# Create your models here.
class Resource(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField()
    category = models.CharField(max_length=50)  # e.g., 'Stress', 'Anxiety', etc.

    def __str__(self):
        return self.title
