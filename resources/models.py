from django.db import models

class Resource(models.Model):
    CATEGORY_CHOICES = [
        ('stress', 'Stress Management'),
        ('sleep', 'Sleep Improvement'),
        ('mindfulness', 'Mindfulness & Meditation'),
        ('general', 'General Mental Health'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField()  # Link to the resource
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
