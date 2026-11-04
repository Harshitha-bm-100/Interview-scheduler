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
        start_time = cleaned.get('start_time')
        end_time = cleaned.get('end_time')


        if not interviewers or start_time is None or end_time is None:
            return cleaned

        if end_time <= start_time:
            raise forms.ValidationError('End time must be after start time.')

        for name in interviewers.split(','):
            name = name.strip()
            if not name:
                continue
            if not InterviewSlot.objects.filter(Interviewer=name).exists():
                raise forms.ValidationError('No availability row for ' + name)
            slot = InterviewSlot.objects.get(Interviewer=name)
            if slot.start_time > start_time or slot.end_time < end_time:
                raise forms.ValidationError('Interviewer ' + name + ' is not free during that time.')
        return cleaned
