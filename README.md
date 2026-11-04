# Interview Scheduler

Version 1. Schedule an interview when the named interviewers are free, then see every saved interview in a table.

## Description

Interview Scheduler is a small Django app. The home page is a form with interviewers, candidate, date, start time, and end time. Date is chosen from month, day, and year menus. Start time and end time are chosen in 30-minute steps. Several interviewers go in one field, separated by commas.

Each interviewer must already have one free window, stored as an interview slot. The interview start and end must sit inside that window, and the end must be after the start. Saving the interview keeps the row and moves each person's free window forward to the interview end. The view page lists every interview with the same columns as the form: interviewers, candidate, date, start time, and end time.

Interviewers are added in Django admin, not on the home page. Create an admin account, open Interview slots, and save a name with a start time and an end time. The name on the form must match that slot exactly.

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
4. Under Scheduling, add an Interview slot for each interviewer: name, start time, and end time.
5. Open http://127.0.0.1:8000/, fill in the form, and press Save.
6. The view page at http://127.0.0.1:8000/view/ shows the saved interviews.

Stop the server with Ctrl+C.

To change the admin password later:

```bash
python manage.py changepassword <username>
```

## Authors

- [Harshitha-bm-100](https://github.com/Harshitha-bm-100)

## Version History

- 1.0
  - Home form to schedule an interview against interviewer free windows
  - View page table of saved interviews
  - Admin pages for interviews and interview slots
