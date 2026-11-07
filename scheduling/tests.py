from datetime import time

from django.test import TestCase

from scheduling.forms import InterviewForm
from scheduling.models import Interview, Interviewer, InterviewSlot


class InterviewFormTests(TestCase):
    def setUp(self):
        self.interviewer = Interviewer.objects.create(name='Ada')
        InterviewSlot.objects.create(
            interviewer=self.interviewer,
            start_time=time(9, 0),
            end_time=time(17, 0),
        )

    def form_data(self, candidate, day):
        return {
            'interviewers': [str(self.interviewer.pk)],
            'candidate': candidate,
            'date_year': '2026',
            'date_month': '1',
            'date_day': str(day),
            'start_time': '10:30',
            'end_time': '11:30',
        }

    def test_interviewer_can_only_be_booked_once_at_a_time_per_day(self):
        first_form = InterviewForm(data=self.form_data('Charles', 3))
        self.assertTrue(first_form.is_valid(), first_form.errors)
        first_form.save()

        overlapping_form = InterviewForm(data=self.form_data('Diana', 3))
        self.assertFalse(overlapping_form.is_valid())

        next_day_form = InterviewForm(data=self.form_data('Naina', 4))
        self.assertTrue(next_day_form.is_valid(), next_day_form.errors)
        next_day_form.save()
        self.assertEqual(Interview.objects.count(), 2)

    def test_editing_interview_does_not_conflict_with_itself(self):
        form = InterviewForm(data=self.form_data('Charles', 3))
        self.assertTrue(form.is_valid(), form.errors)
        interview = form.save()

        edit_form = InterviewForm(
            data=self.form_data('Charles', 3),
            instance=interview,
        )
        self.assertTrue(edit_form.is_valid(), edit_form.errors)

    def test_models_have_string_representations(self):
        form = InterviewForm(data=self.form_data('Charles', 3))
        self.assertTrue(form.is_valid(), form.errors)
        interview = form.save()

        self.assertEqual(str(interview), 'Charles - 2026-01-03')
        self.assertEqual(str(self.interviewer.slot), 'Ada')
