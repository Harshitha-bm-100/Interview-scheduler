from django.db import models

# A saved booking. The date lives here, so each day is a separate row.
# An empty day has no row. Nothing is stored ahead of time for that date.
class Interview(models.Model):
    interviewers = models.ManyToManyField("Interviewer", related_name="interviews")
    candidate = models.CharField(max_length=200)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ['date', 'start_time']

    def __str__(self):
        return f'{self.candidate} - {self.date}'


# One row per person, with no date. These hours apply every day.
# A booking does not change this row. Taken time is recorded on Interview.
class InterviewSlot(models.Model):
    interviewer = models.OneToOneField(
        "Interviewer",
        on_delete=models.CASCADE,
        related_name="slot",
    )
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return str(self.interviewer)


class Interviewer(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name