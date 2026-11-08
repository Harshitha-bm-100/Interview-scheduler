import json

from django.shortcuts import get_object_or_404, redirect, render
from django.db import transaction
from django.http import HttpResponse, JsonResponse

from .forms import InterviewAPIForm, InterviewForm
from .models import Interview
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def _interview_json(interview):
    # Return JSON-safe strings for the model's date and time fields.
    interviewers = []
    for interviewer in interview.interviewers.all():
        interviewers.append({
            'id': interviewer.pk,
            'name': interviewer.name,
        })

    return {
        'id': interview.pk,
        'candidate': interview.candidate,
        'date': interview.date.isoformat(),
        'start_time': interview.start_time.isoformat(),
        'end_time': interview.end_time.isoformat(),
        'interviewers': interviewers,
    }


def APIInterviews(request):
    if request.method == 'GET':
        interviews = (
            Interview.objects
            .prefetch_related('interviewers')
            .order_by('date', 'start_time', 'pk')
        )
        # Return at most 10 interviews per page, defaulting to page 1.
        paginator = Paginator(interviews, 10)
        page = paginator.get_page(request.GET.get('page', 1))

        # Include pagination metadata so API clients can request the next page.
        return JsonResponse({
            'page': page.number,
            'total_pages': paginator.num_pages,
            'has_next': page.has_next(),
            'has_previous': page.has_previous(),
            'results': [_interview_json(interview) for interview in page],
        })

    if request.method != 'POST':
        return JsonResponse(
            {'error': 'Method not allowed.'},
            status=405,
            headers={'Allow': 'GET, POST'},
        )

    if not request.user.is_authenticated:
        return JsonResponse(
            {'error': 'Login required.'},
            status=403,
        )

    # Parse the JSON body before passing values through Django's normal field validation.
    try:
        payload = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({'error': 'Request body must contain valid JSON.'}, status=400)

    if not isinstance(payload, dict):
        return JsonResponse({'error': 'JSON body must be an object.'}, status=400)

    form = InterviewAPIForm(payload)
    if not form.is_valid():
        return JsonResponse({'errors': form.errors.get_json_data()}, status=400)

    # Save the interview and its many-to-many interviewer links together.
    with transaction.atomic():
        data = form.cleaned_data
        interview = Interview.objects.create(
            candidate=data['candidate'],
            date=data['date'],
            start_time=data['start_time'],
            end_time=data['end_time'],
        )
        interview.interviewers.set(data['interviewers'])

    return JsonResponse(_interview_json(interview), status=201)


def APIDelete(request, interview_id):


    if request.method != 'POST':
        return JsonResponse(
            {'error': 'Method not allowed.'},
            status=405,
            headers={'Allow': 'POST'},
        )
    if not request.user.is_authenticated:
        return JsonResponse(
            {'error': 'Login required.'},
            status=403,
        )

    try:
        interview = Interview.objects.get(pk=interview_id)
    except Interview.DoesNotExist:
        return JsonResponse({'error': 'Interview not found.'}, status=404)

    interview.delete()
    return HttpResponse(status=204)

@login_required
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

#order_by
#pagination - request.GET.get('page', 1) reads the page value from the URL query string.
#For example, /view/?page=2 returns "2". If the URL has no page parameter, it returns 1, so the first page is shown by default.

def View(request):
    interviews = (
        Interview.objects
        .prefetch_related('interviewers')
        .order_by('date', 'start_time', 'pk')
    )
    paginator = Paginator(interviews, 10)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    return render(request, 'scheduling/view_page.html', {
        'page': page,
    })



@login_required
def Delete(request, interview_id):
    if request.method == 'POST':
        interview = get_object_or_404(Interview, id=interview_id)
        interview.delete()
    return redirect('view')

@login_required
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
