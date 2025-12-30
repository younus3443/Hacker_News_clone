# core/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from urllib.parse import urlparse

class CustomUser(AbstractUser):
    karma = models.IntegerField(default=0)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username
    


class Submission(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField(blank=True)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="submissions")
    points = models.IntegerField(default=0)
    
    STORY = 'story'
    ASK = 'ask'
    JOB = 'job'
    
    TYPE_CHOICES = [
        (STORY, 'Story'),
        (ASK, 'Ask'),
        (JOB, 'Job'),
    ]
    
    submission_type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default=STORY
    )

    def __str__(self):
        return self.title
    
    @property
    def domain(self):
        if not self.url:
            return None

        parsed = urlparse(self.url)
        domain = parsed.netloc.replace("www.", "")

        # OPTIONAL: include first path segment like github.com/user
        if domain == "github.com":
            path = parsed.path.strip("/").split("/")
            if path:
                domain += f"/{path[0]}"

        return domain
    
class Vote(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE,
        related_name="votes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "submission")  # 🔒 one vote per user

    def __str__(self):
        return f"{self.user} → {self.submission}"
