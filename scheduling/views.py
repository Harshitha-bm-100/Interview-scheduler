from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import (
    AvailabilityWindowForm,
    InterviewForm,
    JobOpeningForm,
    RegisterForm,
)
from .models import Application, AvailabilityWindow, JobOpening


def opening_list(request):
    # JobOpening.Meta.ordering is newest first.
    openings = JobOpening.objects.select_related('recruiter')
    return render(request, 'scheduling/opening_list.html', {'openings': openings})


def opening_detail(request, pk):
    opening = get_object_or_404(JobOpening.objects.select_related('recruiter'), pk=pk)
    applied = False
    if request.user.is_authenticated:
        applied = opening.application_set.filter(candidate=request.user).exists()

    # The recruiter who owns the opening can see who applied.
    applications = []
    if request.user.is_authenticated and request.user == opening.recruiter:
        applications = opening.application_set.select_related('candidate')

    can_apply = (
        request.user.is_authenticated
        and request.user.role == 'candidate'
        and opening.deadline >= timezone.localdate()
        and not applied
    )
    return render(request, 'scheduling/opening_detail.html', {
        'opening': opening,
        'applied': applied,
        'can_apply': can_apply,
        'applications': applications,
    })


@login_required
def opening_create(request):
    # request.POST or None builds a bound form on submit and an empty one on GET.
    form = JobOpeningForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        opening = form.save()
        messages.success(request, 'Job opening saved.')
        return redirect('opening_detail', pk=opening.pk)
    return render(request, 'scheduling/form_page.html', {
        'form': form,
        'title': 'New job opening',
        'submit_label': 'Save opening',
    })


def register(request):
    if request.user.is_authenticated:
        return redirect('opening_list')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Account created. You can log in.')
        return redirect('login')
    return render(request, 'scheduling/form_page.html', {
        'form': form,
        'title': 'Register',
        'submit_label': 'Create account',
    })


class UserLoginView(LoginView):
    """Django's login view. It uses AuthenticationForm, so there is no login form class."""

    template_name = 'scheduling/form_page.html'
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Log in'
        context['submit_label'] = 'Log in'
        return context


@login_required
@require_POST
def apply(request, pk):
    """Apply does not use a form. The view creates the Application row."""

    opening = get_object_or_404(JobOpening, pk=pk)
    if request.user.role != 'candidate':
        messages.error(request, 'Only a candidate can apply.')
        return redirect('opening_detail', pk=pk)
    if opening.deadline < timezone.localdate():
        messages.error(request, 'The deadline for this opening has passed.')
        return redirect('opening_detail', pk=pk)

    already_applied = Application.objects.filter(
        candidate=request.user,
        applied_job=opening,
    ).exists()
    if already_applied:
        messages.info(request, 'You already applied for this opening.')
        return redirect('opening_detail', pk=pk)

    # candidate is the logged-in user. applied_job is the opening they clicked.
    Application.objects.create(candidate=request.user, applied_job=opening)
    messages.success(request, 'Application saved.')
    return redirect('opening_detail', pk=pk)


@login_required
def schedule_interview(request, pk):
    application = get_object_or_404(
        Application.objects.select_related('candidate', 'applied_job'),
        pk=pk,
    )
    if request.method == 'POST':
        form = InterviewForm(request.POST, application=application)
        if form.is_valid():
            form.save()
            messages.success(request, 'Interview scheduled.')
            return redirect('opening_detail', pk=application.applied_job_id)
    else:
        form = InterviewForm(application=application)
    return render(request, 'scheduling/form_page.html', {
        'form': form,
        'title': 'Schedule interview',
        'submit_label': 'Schedule',
        'intro': f'{application.candidate.username} applied for {application.applied_job.position}.',
    })


@login_required
def availability_create(request):
    form = AvailabilityWindowForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Free time saved.')
        return redirect('availability_create')

    # Show this interviewer's windows under the form. Others see every window.
    if request.user.role == 'interviewer':
        windows = AvailabilityWindow.objects.filter(interviewer=request.user)
    else:
        windows = AvailabilityWindow.objects.select_related('interviewer')
    windows = windows.order_by('starts_at')
    return render(request, 'scheduling/availability.html', {
        'form': form,
        'windows': windows,
    })
