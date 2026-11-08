from datetime import time
import json

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


class InterviewAPITests(TestCase):
    def setUp(self):
        self.interviewer = Interviewer.objects.create(name='Ada')
        InterviewSlot.objects.create(
            interviewer=self.interviewer,
            start_time=time(9, 0),
            end_time=time(17, 0),
        )
        self.payload = {
            'interviewers': [self.interviewer.pk],
            'candidate': 'Charles',
            'date': '2026-01-03',
            'start_time': '10:30',
            'end_time': '11:30',
        }

    def post_json(self, url, payload):
        return self.client.post(
            url,
            data=json.dumps(payload),
            content_type='application/json',
        )

    def test_list_interviews_returns_json(self):
        response = self.post_json('/api/interviews/', self.payload)
        self.assertEqual(response.status_code, 201)

        response = self.client.get('/api/interviews/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['candidate'], 'Charles')
        self.assertEqual(response.json()[0]['date'], '2026-01-03')

    def test_create_uses_shared_booking_validation(self):
        self.assertEqual(self.post_json('/api/interviews/', self.payload).status_code, 201)

        overlapping_payload = {**self.payload, 'candidate': 'Diana'}
        response = self.post_json('/api/interviews/', overlapping_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Interview.objects.count(), 1)

    def test_invalid_json_and_invalid_fields_return_bad_request(self):
        response = self.client.post(
            '/api/interviews/',
            data='{not json',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)

        response = self.post_json('/api/interviews/', {'candidate': 'Incomplete'})
        self.assertEqual(response.status_code, 400)

    def test_delete_returns_no_content(self):
        response = self.post_json('/api/interviews/', self.payload)
        interview_id = response.json()['id']

        response = self.client.post(f'/api/interviews/{interview_id}/delete/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Interview.objects.count(), 0)
