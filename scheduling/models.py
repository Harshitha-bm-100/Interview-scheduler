from django.db import models

# Create your models here.
class Interview(models.Model):
    interviewers = models.CharField(max_length=200)
    candidate = models.CharField(max_length=200)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ['date', 'start_time']

    def __str__(self):
        return self.interviewers
    
class InterviewSlot(models.Model):
    # One row: this person is free from start_time until end_time.
    Interviewer = models.CharField(max_length=200)
    start_time = models.TimeField()
    end_time = models.TimeField()


    def __str__(self):
        return self.Interviewer