from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import AvailabilityWindow, Interview, JobOpening, User


class RegisterForm(UserCreationForm):
    """Sign-up form. Any person can use it.

    Role is not on the form. User.role defaults to candidate, so a new
    account starts as a candidate.
    """

    class Meta:
        model = User
        # This list is the order of the boxes on the page.
        # password1 and password2 come from UserCreationForm.
        fields = ['username', 'email', 'password1', 'password2']


class JobOpeningForm(forms.ModelForm):
    """Form for one job opening.

    Showing every opening on a page is a view, not this form.
    This form is the fields for a single opening.
    """

    class Meta:
        model = JobOpening
        # Order here is the order on the page.
        fields = ['recruiter', 'position', 'description', 'deadline']
        widgets = {
            # Browser date picker instead of a plain text box.
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }


class InterviewForm(forms.ModelForm):
    """Schedule one interview for an application.

    The view already knows the application, so it is not a field here.
    Pass it in when creating the form:

        form = InterviewForm(request.POST, application=application)
    """

    class Meta:
        model = Interview
        # Order here is the order on the page.
        fields = ['interviewer', 'starts_at', 'ends_at']
        widgets = {
            'starts_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'ends_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, application=None, **kwargs):
        # Kept so save() can attach this interview to the right application.
        self.application = application
        super().__init__(*args, **kwargs)
        # datetime-local sends "2026-11-03T14:30". Teach the fields that shape.
        for name in ('starts_at', 'ends_at'):
            self.fields[name].input_formats = ['%Y-%m-%dT%H:%M', '%Y-%m-%dT%H:%M:%S']

    def clean(self):
        cleaned = super().clean()
        interviewer = cleaned.get('interviewer')
        starts_at = cleaned.get('starts_at')
        ends_at = cleaned.get('ends_at')
        if not interviewer or not starts_at or not ends_at:
            return cleaned

        if ends_at <= starts_at:
            raise forms.ValidationError('The interview must end after it starts.')

        # The whole interview must sit inside one free window.
        window = AvailabilityWindow.objects.filter(
            interviewer=interviewer,
            starts_at__lte=starts_at,
            ends_at__gte=ends_at,
        ).first()
        if window is None:
            raise forms.ValidationError('That interviewer is not free for the whole interview.')

        self.matching_window = window
        return cleaned

    def save(self, commit=True):
        interview = super().save(commit=False)
        if self.application is not None:
            interview.application = self.application
        if commit:
            interview.save()
            # The interviewer is now busy, so remove this time from their window.
            self._take_time_from_window()
        return interview

    def _take_time_from_window(self):
        window = self.matching_window
        start = self.cleaned_data['starts_at']
        end = self.cleaned_data['ends_at']

        # Interview uses the whole window.
        if window.starts_at == start and window.ends_at == end:
            window.delete()
            return

        # Interview starts when the window starts. Keep the time after it.
        if window.starts_at == start:
            window.starts_at = end
            window.save()
            return

        # Interview ends when the window ends. Keep the time before it.
        if window.ends_at == end:
            window.ends_at = start
            window.save()
            return

        # Interview is in the middle. Split the window into before and after.
        AvailabilityWindow.objects.create(
            interviewer=window.interviewer,
            starts_at=end,
            ends_at=window.ends_at,
        )
        window.ends_at = start
        window.save()


class AvailabilityWindowForm(forms.ModelForm):
    """Free time for one interviewer.

    InterviewForm can schedule someone only inside a window saved here.
    """

    class Meta:
        model = AvailabilityWindow
        # Order here is the order on the page.
        fields = ['interviewer', 'starts_at', 'ends_at']
        widgets = {
            'starts_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'ends_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # datetime-local sends "2026-11-03T14:30". Teach the fields that shape.
        for name in ('starts_at', 'ends_at'):
            self.fields[name].input_formats = ['%Y-%m-%dT%H:%M', '%Y-%m-%dT%H:%M:%S']

    def clean(self):
        cleaned = super().clean()
        interviewer = cleaned.get('interviewer')
        starts_at = cleaned.get('starts_at')
        ends_at = cleaned.get('ends_at')
        if not interviewer or not starts_at or not ends_at:
            return cleaned

        if ends_at <= starts_at:
            raise forms.ValidationError('Free time must end after it starts.')

        # Two windows for the same person should not cover the same time.
        overlap = AvailabilityWindow.objects.filter(
            interviewer=interviewer,
            starts_at__lt=ends_at,
            ends_at__gt=starts_at,
        )
        if self.instance.pk:
            overlap = overlap.exclude(pk=self.instance.pk)
        if overlap.exists():
            raise forms.ValidationError('That interviewer already has free time in this period.')

        return cleaned
