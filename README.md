# Student Management System

A modern Django-based student management system with a beautiful Bootstrap 5 UI.

## Features

- **CRUD Operations**: Create, Read, Update, and Delete students
- **Search Functionality**: Search students by name, email, or course
- **Modern UI**: Clean, responsive design with Bootstrap 5
- **Admin Panel**: Full-featured Django admin interface
- **Student Dashboard**: Overview with statistics

## Student Fields

- First Name & Last Name
- Email (unique)
- Phone Number
- Date of Birth
- Gender
- Address
- Course
- Grade (A+ to F)
- GPA (0.00 - 4.00)
- Active Status

## Setup Instructions

### 1. Create and Activate Virtual Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate (PowerShell)
.\venv\Scripts\Activate.ps1

# Activate (Command Prompt)
.\venv\Scripts\activate.bat
```

### 2. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 3. Run Migrations

```powershell
python manage.py migrate
```

### 4. Create Superuser (for Admin Panel)

```powershell
python manage.py createsuperuser
```

### 5. Run Development Server

```powershell
python manage.py runserver
```

### 6. Access the Application

- **Main Application**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## Project Structure

```
student_management/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── student_management/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── students/
    ├── models.py
    ├── views.py
    ├── forms.py
    ├── urls.py
    ├── admin.py
    └── templates/
        └── students/
            ├── base.html
            ├── student_list.html
            ├── student_detail.html
            ├── student_form.html
            └── student_confirm_delete.html
```

## Technologies Used

- **Backend**: Django 5.2
- **Frontend**: Bootstrap 5.3, Bootstrap Icons
- **Database**: SQLite (default)
- **Fonts**: Google Fonts (Inter)
