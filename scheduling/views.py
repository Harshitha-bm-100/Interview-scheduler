from django.shortcuts import get_object_or_404, redirect, render

from .forms import InterviewForm
from .models import Interview


def Home(request):
    if request.method == 'POST':
        form = InterviewForm(request.POST)
        if form.is_valid():
            # Saves the Interview, including its date. The slot row is left as entered.
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
