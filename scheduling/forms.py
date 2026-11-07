from datetime import time

from django import forms

from .models import Interview, InterviewSlot

TIME_CHOICES = [('', '---------')] + [
    (time(hour, minute).strftime('%H:%M'), f'{hour:02d}:{minute:02d}')
    for hour in range(24)
    for minute in (0, 30)
]


class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['interviewers', 'candidate', 'date', 'start_time', 'end_time']
        widgets = {
            'date': forms.SelectDateWidget(empty_label=('Year', 'Month', 'Day')),
            'start_time': forms.Select(choices=TIME_CHOICES),
            'end_time': forms.Select(choices=TIME_CHOICES),
        }

    def clean(self):
        cleaned = super().clean()
        interviewers = cleaned.get('interviewers')
        interview_date = cleaned.get('date')
        start_time = cleaned.get('start_time')
        end_time = cleaned.get('end_time')

        # A missing field is already reported by the form. Stop here.
        if not interviewers or interview_date is None or start_time is None or end_time is None:
            return cleaned

        if end_time <= start_time:
            raise forms.ValidationError('End time must be after start time.')

        for interviewer in interviewers.all():
            slot = InterviewSlot.objects.filter(interviewer=interviewer).first()
            if slot is None:
                raise forms.ValidationError('No availability row for ' + str(interviewer))
            if slot.start_time > start_time or slot.end_time < end_time:
                raise forms.ValidationError('Interviewer ' + str(interviewer) + ' is not free during that time.')

            already_booked = Interview.objects.filter(
                date=interview_date,
                start_time__lt=end_time,
                end_time__gt=start_time,
                interviewers=interviewer,
            )
            # When editing, don't treat this interview's existing row as a conflict.
            if self.instance.pk:
                already_booked = already_booked.exclude(pk=self.instance.pk)
            # Reject the form if any other booking overlaps this interview's time.
            if already_booked.exists():
                raise forms.ValidationError(
                    'Interviewer ' + str(interviewer) + ' is already booked during that time on that date.'
                )
        return cleaned
