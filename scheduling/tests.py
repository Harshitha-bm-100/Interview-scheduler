from django.test import TestCase
from scheduling.models import InterviewSlot
from datetime import time, date
from scheduling.forms import InterviewForm

# Create your tests here.
class InterviewSlotTestCase(TestCase):
    def test_interview_slot_creation(self):
        InterviewSlot.objects.create(
            Interviewer = 'Ada',
            start_time = time(9, 0),
            end_time = time(17, 0),
        )

        first_form = InterviewForm(data={
            'interviewers': 'Ada',
            'candidate': 'Charles',
            'date': date(2026, 1, 3),
            'start_time': time(10, 30),
            'end_time': time(11, 30),
        })

        #should accept
        self.assertTrue(first_form.is_valid())
        first_form.save()

        second_form = InterviewForm(data={
            'interviewers': 'Ada',
            'candidate': 'Diana',
            'date': date(2026, 1, 3),
            'start_time': time(10, 30),
            'end_time': time(11, 30),
        })

        #should reject
        self.assertFalse(second_form.is_valid())

        next_day_form = InterviewForm(data={
            'interviewers': 'Ada',
            'candidate': 'Naina',
            'date': date(2026, 1, 4),
            'start_time': time(10, 30),
            'end_time': time(11, 30),
        })
        #should accept
        self.assertTrue(next_day_form.is_valid())
        next_day_form.save()








