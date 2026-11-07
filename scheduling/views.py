from django.shortcuts import get_object_or_404, redirect, render
from django.db import transaction

from .forms import InterviewForm
from .models import Interview


def Home(request):
    if request.method == 'POST':
        form = InterviewForm(request.POST)
        # SQLite uses BEGIN IMMEDIATE; use select_for_update() on databases with row-level locks.
        with transaction.atomic():
            if form.is_valid():
                form.save()
                return redirect('view')
    else:
        form = InterviewForm()
    return render(request, 'scheduling/home_page.html', {
        'form': form,
    })


def View(request):
    return render(request, 'scheduling/view_page.html', {
        'interviews': Interview.objects.all(),
    })


def Delete(request, interview_id):
    if request.method == 'POST':
        interview = get_object_or_404(Interview, id=interview_id)
        interview.delete()
    return redirect('view')

def Edit(request, interview_id):
    interview = get_object_or_404(Interview, id=interview_id)
    if request.method == 'POST':
        #instance is the existing interview row the form should change.
        #Without it, InterviewForm builds a new empty booking and save() inserts a second row.
        form = InterviewForm(request.POST, instance=interview)
        if form.is_valid():
            form.save()
            return redirect('view')
    else:
        form = InterviewForm(instance=interview)
    return render(request, 'scheduling/edit_page.html', {
        'form': form,
    })
