from datetime import time

from django import forms

from .models import Interview, Interviewer

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
            'interviewers': forms.CheckboxSelectMultiple(),
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

        self.instance.check_can_book(interviewers, interview_date, start_time, end_time)

        return cleaned


class InterviewAPIForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = [
            'interviewers',
            'candidate',
            'date',
            'start_time',
            'end_time',
        ]

    def clean(self):
        cleaned = super().clean()

        interviewers = cleaned.get('interviewers')
        interview_date = cleaned.get('date')
        start_time = cleaned.get('start_time')
        end_time = cleaned.get('end_time')

        if interviewers and interview_date and start_time and end_time:
            booking = Interview(
                candidate=cleaned.get('candidate', ''),
                date=interview_date,
                start_time=start_time,
                end_time=end_time,
            )
            booking.check_can_book(
                interviewers,
                interview_date,
                start_time,
                end_time,
            )

        return cleaned
