from django.shortcuts import redirect, render

from .forms import InterviewForm
from .models import Interview, InterviewSlot


def Home(request):
    if request.method == 'POST':
        form = InterviewForm(request.POST)
        if form.is_valid():
            form.save()
            # The interview used the beginning of each person's free window.
            # Move start_time forward to the interview end. end_time stays.
            for name in form.cleaned_data['interviewers'].split(','):
                name = name.strip()
                slot = InterviewSlot.objects.get(Interviewer=name)
                slot.start_time = form.cleaned_data['end_time']
                slot.save()
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
