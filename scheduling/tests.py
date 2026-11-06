from django.test import TestCase
from scheduling.models import InterviewSlot, Interview
from datetime import time, date
from scheduling.forms import InterviewForm

# Create your tests here.
#add an interview

#TestCase is Django's test base class. 
#A class that inherits it gets a fresh database for each test, the setUp method runs before each one
class InterviewSlotSetup(TestCase):
    def setUp(self):
        InterviewSlot.objects.create(
            Interviewer='Ada',
            start_time=time(9, 0),
            end_time=time(17, 0),
        )

#Django's test runner only runs methods whose names start with test_. That is how it tells a test apart from a helper. 
#setUp creates Ada's slot and is not a test, so it does not start with test_
class AddInterview(InterviewSlotSetup):
    def test_add_interview(self):
    
        self.client.post('/', {
            'interviewers': 'Ada',
            'candidate': 'Charles',
            'date': date(2026, 1, 3),
            'start_time': time(10, 30),
            'end_time': time(11, 30),
        })

        self.assertEqual(Interview.objects.count(), 1)

class DeleteInterview(InterviewSlotSetup):
    def test_delete_interview(self):
        AddInterview.test_add_interview(self)
        interview = Interview.objects.get(candidate='Charles')
        self.client.post(f'/delete/{interview.id}/')
        self.assertEqual(Interview.objects.count(), 0)


        
class InterviewSlotTestCase(InterviewSlotSetup):
    def test_interview_slot_creation(self):

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

        #should reject - requires the form to be invalid
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

    







