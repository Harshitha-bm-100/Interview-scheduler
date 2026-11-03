from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = [
        ('candidate', 'Candidate'),
        ('recruiter', 'Recruiter'),
        ('interviewer', 'Interviewer'),
    ]

    role = models.CharField(max_length = 200, choices = ROLE_CHOICES, default='candidate')


class JobOpening(models.Model):
    recruiter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='job_openings',
        limit_choices_to={'role': 'recruiter'},
    )
    position = models.CharField(max_length = 200)
    description = models.TextField()
    # Last day a candidate can apply for this opening.
    deadline = models.DateField()
    # Set once, when the opening is first saved.
    created_at = models.DateTimeField(auto_now_add=True)
    interviewers = models.ManyToManyField(
        User,
        related_name='assigned_openings',
        limit_choices_to={'role': 'interviewer'},
        blank=True,
    )

    class Meta:
        # Newest opening first whenever a list of openings is loaded.
        ordering = ['-created_at']


class Application(models.Model):
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'candidate'})
    applied_job = models.ForeignKey(JobOpening, on_delete=models.CASCADE)

class AvailabilityWindow(models.Model):
    interviewer =  models.ForeignKey(User, on_delete=models.CASCADE,limit_choices_to={"role": "interviewer"})
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()

class Interview(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    interviewer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': "interviewer"})
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()








    



