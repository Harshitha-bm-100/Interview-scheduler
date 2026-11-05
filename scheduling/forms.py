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

        for name in interviewers.split(','):
            name = name.strip()
            if not name:
                continue

            # The slot has no date. Look it up by name only.
            if not InterviewSlot.objects.filter(Interviewer=name).exists():
                raise forms.ValidationError('No availability row for ' + name)
            slot = InterviewSlot.objects.get(Interviewer=name)
            if slot.start_time > start_time or slot.end_time < end_time:
                raise forms.ValidationError('Interviewer ' + name + ' is not free during that time.')

            # Taken times for this day are other Interview rows with the same date.
            already_booked = Interview.objects.filter(
                date=interview_date,
                start_time__lt=end_time,
                end_time__gt=start_time,
            )
            for interview in already_booked:
                booked_names = [part.strip() for part in interview.interviewers.split(',')]
                if name in booked_names:
                    raise forms.ValidationError(
                        'Interviewer ' + name + ' is already booked during that time on that date.'
                    )
        return cleaned
