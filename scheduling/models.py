from django.db import models
from django.core.exceptions import ValidationError

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
        indexes = [
            models.Index(fields=['date', 'start_time'], name='interview_date_start_idx'),
        ]

    def check_can_book(self, interviewers, interview_date, start_time, end_time):
        # Missing values are already reported by the form's field validation.
        if not interviewers or interview_date is None or start_time is None or end_time is None:
            return

        # Require a positive-duration interview.
        if end_time <= start_time:
            raise ValidationError('End time must be after start time.')

        # Every selected interviewer must be free for the full requested time.
        for interviewer in interviewers:
            slot = InterviewSlot.objects.filter(interviewer=interviewer).first()
            if slot is None:
                raise ValidationError('No availability row for ' + str(interviewer))
            if slot.start_time > start_time or slot.end_time < end_time:
                raise ValidationError(
                    'Interviewer ' + str(interviewer) + ' is not free during that time.'
                )

            # Reject overlapping bookings on the same date, except this interview when editing.
            already_booked = Interview.objects.filter(
                date=interview_date,
                start_time__lt=end_time,
                end_time__gt=start_time,
                interviewers=interviewer,
            )
            if self.pk:
                already_booked = already_booked.exclude(pk=self.pk)
            if already_booked.exists():
                raise ValidationError(
                    'Interviewer ' + str(interviewer) + ' is already booked during that time on that date.'
                )

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