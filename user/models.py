from django.db import models
from django.contrib.auth.models import AbstractUser
from user.managers import CustomUserManager
import uuid
from django.core.files.storage import default_storage
GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('None', 'Prefer not to say.'),
]

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)
    full_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    is_private_account = models.BooleanField(default=False)
    website = models.URLField(null=True, blank=True)
    first_name = None
    last_name = None
    REQUIRED_FIELDS = ['full_name','username']
    USERNAME_FIELD = 'email'
    objects =  CustomUserManager()
    def __str__(self) -> str:
        return self.email
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid.uuid4()
        return super().save(*args, **kwargs)
    
    @property
    def follower_count(self):
        count = self.follow_follower.count()
        return count
    
    @property   
    def following_count(self):
        count = self.follow_user.count()
        return count
