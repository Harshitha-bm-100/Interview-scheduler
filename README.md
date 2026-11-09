# Interview Scheduler

Version 1. Schedule an interview with one or more interviewers, then see, edit, or delete the saved interviews.

## Description

Interview Scheduler is a small Django app for booking interviews.

People and their hours are set up in Django admin:

- An **interviewer** is one person, stored by name.
- An **interview slot** is that person's free window. Each person has one slot. It has a start time and an end time, and no date, so the same hours apply every day. Saving an interview does not change the slot.

The home page is a form:

- Interviewers are a scrolling list of checkboxes. Select one or more people.
- Candidate is a name.
- Date is chosen from month, day, and year menus.
- Start time and end time are chosen in 30-minute steps.

Save is accepted only when the booking fits:

- The end time is after the start time.
- Every selected interviewer has a slot, and the interview sits inside that daily window.
- None of those people already has an overlapping interview on that date.

A booking uses the slot as the daily window and stores the taken time on the interview. The same hours can be booked again on another date. Editing an interview does not treat that interview as a conflict with itself.

The view page lists interviews in a table: interviewers, candidate, date, start time, and end time. The list is ordered by date and start time, with 10 rows per page. A signed-in user can edit or delete a row. The edit page uses the same form as the home page, with the current people left checked.

Scheduling, editing, and deleting require a signed-in user. The view page can be opened without signing in.

## Getting Started

### Dependencies

- Python 3
- pip
- Git

Django 6.1.2 is installed from `requirements.txt`. SQLite comes with Python, so you do not install a separate database. The app runs on macOS, Linux, and Windows.

### Installing

Clone the repository and install its dependencies inside a virtual environment.

macOS and Linux:

```bash
git clone https://github.com/Harshitha-bm-100/Interview-scheduler.git
cd Interview-scheduler
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

Windows:

```bash
git clone https://github.com/Harshitha-bm-100/Interview-scheduler.git
cd Interview-scheduler
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

`migrate` creates `db.sqlite3` in the project folder. That file is local. It is listed in `.gitignore`, so it is not part of the clone.

### Executing program

1. Activate the virtual environment if the terminal does not already show `(.venv)`.
2. Start the server:

```bash
python manage.py runserver
```

3. Open http://127.0.0.1:8000/admin/ and sign in with the superuser you created.
4. Under Scheduling, add each interviewer, then add one interview slot for that person with a start time and an end time.
5. Open http://127.0.0.1:8000/ and sign in. Check one or more interviewers, fill in the rest of the form, and press Save.
6. The view page at http://127.0.0.1:8000/view/ shows the saved interviews. Use Edit or Delete on a row to change or remove it.

Stop the server with Ctrl+C.

To change the admin password later:

```bash
python manage.py changepassword <username>
```

## Authors

- [Harshitha-bm-100](https://github.com/Harshitha-bm-100)

## Version History

- 1.0
  - Home form to schedule an interview with one or more interviewers
  - Daily free window per interviewer, stored as an interview slot
  - View page of saved interviews, with edit and delete
  - Admin pages for interviewers, interview slots, and interviews
