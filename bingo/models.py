# Import necessary Django modules for database models
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
import uuid
from datetime import timedelta


# Custom User Model

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Adds a role field to categorize users into different roles.
    """
    ROLE_CHOICES = [
        ('Player', 'Player'),  # Regular players in the game
        ('GameKeeper', 'GameKeeper'),  # Moderators who verify game tasks
        ('Developer', 'Developer'),  # Developers with admin privileges
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='Player',
        blank=True,
        null=True
    )

    email = models.EmailField(unique=True)  # Ensures each user has a unique email

    def __str__(self):
        """Returns the username as the string representation of the user."""
        return self.username


# User Consent Model

class UserConsent(models.Model):
    """
    Model to store GDPR consent information for each user.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="gdprConsent"
    )  # Links consent record to a user

    consented_at = models.DateTimeField(auto_now_add=True)  # Timestamp of consent
    ip_address = models.GenericIPAddressField(null=True, blank=True)  # Stores IP address for legal compliance

    def __str__(self):
        """Returns a formatted string representation of consent details."""
        return f"{self.user.username} - Consent on {self.consented_at}"


# Password Reset Token Model

class PasswordResetToken(models.Model):
    """
    Model to store password reset tokens with expiration times.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reset_tokens'
    )
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    def __str__(self):
        """Returns a formatted string representation of the reset token."""
        return f"Reset token for {self.user.username} - expires {self.expires_at}"

    def save(self, *args, **kwargs):
        # Set expiration to 24 hours from creation if not already set
        if not self.expires_at:
            self.expires_at = now() + timedelta(hours=24)
        super().save(*args, **kwargs)

    @property
    def is_valid(self):
        """Check if token is still valid (not expired and not used)"""
        return not self.used and self.expires_at > now()


# Profile Model

class Profile(models.Model):
    """
    User profile model containing additional details such as profile pictures,
    ranking, and total points.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )  # Links the profile to a user

    profile_picture = models.ImageField(
        upload_to='static/media/profile_pics/',
        null=True,
        blank=True
    )  # Allows users to upload a profile picture

    rank = models.CharField(max_length=50, default="Unranked")  # Stores the user's rank in the game
    total_points = models.IntegerField(default=0)  # Stores total points earned by the user

    def __str__(self):
        """Returns the username as the string representation of the profile."""
        return self.user.username


# Task Model

class Task(models.Model):
    """
    Model representing tasks that players must complete.
    Each task has a description, point value, and conditions for completion.
    """
    description = models.TextField()  # Stores the task description
    points = models.IntegerField()  # The number of points the task is worth
    requires_upload = models.BooleanField(default=False)  # Whether a photo upload is required
    requires_scan = models.BooleanField(default=False)  # Whether scanning a QR code is required

    def __str__(self):
        """Returns the task description as its string representation."""
        return self.description


# UserTask Model

class UserTask(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]
    """
    Model representing a user's progress on specific tasks.
    Tracks task completion and stores proof (photo) if required.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )  # Links the task completion to a specific user

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE
    )  # Links the task completion to a specific task

    completed = models.BooleanField(default=False)  # Whether the user has completed the task
    photo = models.ImageField(
        upload_to='task_photos/',
        blank=True,
        null=True
    )  # Stores a photo if required for verification

    completion_date = models.DateTimeField(auto_now_add=True)  # Timestamp of task completion
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    approval_date = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('user', 'task')


# Leaderboard Model

class Leaderboard(models.Model):
    """Model to track and rank players based on points earned."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)  # Lifetime points
    monthly_points = models.IntegerField(default=0)  # Monthly points
    last_reset = models.DateField(default=now)  # Stores the last reset date

    def __str__(self):
        return f"{self.user.username} - {self.points} Lifetime Points | {self.monthly_points} Monthly Points"

    def reset_monthly_points(self):
        """Resets monthly points at the beginning of each month."""
        self.monthly_points = 0
        self.last_reset = now().date()
        self.save()


class AccessCode(models.Model):
    """Model to store access codes for admin roles"""
    code = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=20, choices=User.ROLE_CHOICES)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role} Access Code - {'Used' if self.is_used else 'Available'}"


class BingoPattern(models.Model):
    """
    Model to store different bingo patterns that can be achieved
    """
    name = models.CharField(max_length=50)  # e.g. "Zero Waste Hero"
    pattern_type = models.CharField(max_length=20)  # e.g. "O", "X", "H", "V"
    description = models.TextField()
    bonus_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.pattern_type})"


class UserBadge(models.Model):
    """
    Model to track badges earned by users
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pattern = models.ForeignKey(BingoPattern, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'pattern')

    def __str__(self):
        return f"{self.user.username} - {self.pattern.name}"


class TaskBonus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    bonus_points = models.IntegerField(default=0)
    reason = models.CharField(max_length=255)
    awarded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'task', 'reason')

    def __str__(self):
        return f"{self.user.username} - {self.bonus_points} points for task #{self.task.id} ({self.reason})"