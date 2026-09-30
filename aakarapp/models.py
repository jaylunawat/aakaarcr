from django.conf import settings
from django.db import models
from django.utils import timezone

# This model appears to be your user profile. Let's keep it for now.
# It's better to link this to Django's User model with a OneToOneField
# but we can address that later.
class TaskZero(models.Model):
    AVATAR_CHOICES = (
        ("rhino-orange", "Rhino — orange"),
        ("black-bear", "Black bear"),
        ("koala", "Koala"),
        ("brown-bear", "Brown bear"),
        ("owl", "Owl"),
        ("deer", "Deer"),
        ("raccoon", "Raccoon"),
        ("fox", "Fox"),
        ("rhino-green", "Rhino — green"),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cr_profile",
        null=True,
        blank=True,
    )
    crid = models.CharField(max_length=10, unique=True)
    names = models.CharField(max_length = 200)
    username = models.CharField(max_length = 200)
    email = models.CharField(max_length = 200)
    emails = models.CharField(max_length = 200)
    colgName = models.CharField(max_length = 200)
    state = models.CharField(max_length = 200)
    city = models.CharField(max_length=200, default='')
    mobileNo = models.CharField(max_length=10)
    dept = models.CharField(max_length = 200)
    whatsappNo = models.CharField(max_length = 10)
    pincode = models.CharField(max_length = 6)
    address = models.CharField(max_length = 200)
    avatar = models.CharField(max_length=20, choices=AVATAR_CHOICES, default="fox")
    academic_year = models.CharField(max_length=60, blank=True)
    is_approved = models.BooleanField(default=False)
    joined_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "CR profile"
        verbose_name_plural = "CR profiles"
        ordering = ("names",)
    
    def __str__(self):
        return f"{self.username} | {self.crid}"

# --- NEW AND IMPROVED MODELS ---

# 1. This model defines what a task is.

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    points = models.IntegerField(default=100)
    # This is the new field for the deadline
    deadline = models.DateTimeField(null=True, blank=True, help_text="Optional: The task will disappear after this date.")
    is_published = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("sort_order", "-id")

# 2. This model stores a user's submission for a specific task.
class Submission(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    link = models.URLField(max_length=200, blank=True, null=True)
    file = models.FileField(upload_to='submissions/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    marks = models.IntegerField(default=0)
    # This new field will track if you have graded the submission
    graded = models.BooleanField(default=False)

    def __str__(self):
        return f"Submission by {self.user.username} for {self.task.title}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("task", "user"), name="one_submission_per_task_user"),
        ]
        ordering = ("-submitted_at",)


class ContactMessage(models.Model):
    """Messages sent from the public contact page for the organising team."""

    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=180)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ("is_resolved", "-created_at")

    def __str__(self):
        return f"{self.subject} — {self.name}"

# We are removing all the old, repetitive models like taskOne, taskTwo, etc.
# The email_auto model seems unused for the task system, so I've removed it for clarity.
# If you use it elsewhere, you can add it back in.
