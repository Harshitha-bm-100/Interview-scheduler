# Interview Scheduler

Schedule interviews around job openings, applications, and interviewer free time.

## Description

Interview Scheduler is a small Django web app for hiring. The home page lists every job opening, newest first. Each row shows the recruiter, position, description, and the last day to apply. Open a row for that one opening. A candidate presses Apply to create an application. The recruiter for that opening sees the applicants and can schedule an interview. An interviewer saves free time first. An interview can be saved only when that person is free for the whole slot, and saving removes that time from their window. A missing id shows a 404 page. The same records are also available in Django admin after you create an admin login.

Register asks for a username, email, and password. A new account starts as a candidate. Recruiter and interviewer accounts are created in admin, where the role is chosen. A job opening needs a recruiter, a position, a description, and a deadline. Free time and interviews need a start and an end, and the end must be after the start.

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
```

Windows:

```bash
git clone https://github.com/Harshitha-bm-100/Interview-scheduler.git
cd Interview-scheduler
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
```

`migrate` creates `db.sqlite3` in the project folder. That file is local. It is listed in `.gitignore`, so it is not part of the clone. No project files need to be edited before the first run.

### Executing program

1. Activate the virtual environment if the terminal does not already show `(.venv)`.
2. Start the server:

```bash
python manage.py runserver
```

3. Open http://127.0.0.1:8000/.
4. Press Register, create an account, and log in.
5. Open an opening and press Apply, or use New opening and Free time from the header.

Optional admin site:

```bash
python manage.py createsuperuser
```

Then open http://127.0.0.1:8000/admin/ and sign in with that account. Under Scheduling, then Users, add a user and set Role to Recruiter or Interviewer.

Stop the server with Ctrl+C.

## Authors

- [Harshitha-bm-100](https://github.com/Harshitha-bm-100)

## Version History

- 0.1
  - Initial release
