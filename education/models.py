from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator

# Model for Uploaded Content (Videos and Notes)
class UploadedContent(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('video', 'Video'),
        ('note', 'Note'),
    ]
    title = models.CharField(max_length=255)  # Title of the content
    description = models.TextField(blank=True)  # Optional description
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPE_CHOICES)  # Type: Video or Note
    file = models.FileField(upload_to='uploads/')  # File upload location
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Reference to the user who uploaded
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Timestamp of upload

    def __str__(self):
        return self.title


# Model for Subjects
class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


# Model for Teacher Profile
class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    bio = models.TextField(blank=True)
    subjects = models.ManyToManyField(Subject, related_name='teachers')
    experience = models.PositiveIntegerField(default=0, help_text="Years of teaching experience")
    qualification = models.CharField(max_length=255, blank=True)
    profile_picture = models.ImageField(upload_to='teacher_profiles/', blank=True, null=True)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}'s Profile"


# Model for Video Content
class VideoContent(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    video_file = models.FileField(
        upload_to='videos/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'webm', 'ogg'])]
    )
    thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True, null=True)
    duration = models.DurationField(help_text="Duration in seconds", null=True, blank=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, related_name='videos')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


# Model for Notes
class Note(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    file = models.FileField(upload_to='notes/', blank=True, null=True)
    video = models.ForeignKey(VideoContent, on_delete=models.CASCADE, related_name='notes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Notes for {self.video.title}"


# Model for User Profile (to differentiate between Students and Teachers)
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    
    # Student specific fields
    grade = models.CharField(max_length=20, blank=True)
    
    # Teacher specific fields will be in TeacherProfile
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    @property
    def is_teacher(self):
        return self.role == 'teacher'
    
    @property
    def is_student(self):
        return self.role == 'student'


# Signal to automatically create a UserProfile when a User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


# Signal to save the UserProfile whenever the User is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs): instance.userprofile.save()