# Student Management System (India)

A comprehensive Django-based Student Management System designed for Indian educational institutions with modern Bootstrap 5 UI.

## Features

### Core Features
- **Student Management** - Complete CRUD operations with Indian-specific fields
- **Course Management** - Manage courses, credits, and semester assignments
- **Department Management** - Organize academic departments
- **Attendance Tracking** - Daily attendance with multiple status options
- **Fee Management** - Track fees in Indian Rupees (₹) with multiple payment modes
- **User Authentication** - Login/Signup system with role-based access
- **Dashboard Analytics** - Visual charts and statistics
- **Export to Excel** - Download student and attendance data

### Indian-Specific Features
- Aadhaar Number validation
- Caste Category (General, OBC, SC, ST, EWS)
- All Indian States and Union Territories
- Education Board selection (CBSE, ICSE, State Board, etc.)
- 10th & 12th class details with percentage
- Indian mobile number validation (+91)
- PIN code validation (6 digits)
- Family income tracking
- Parent details (Father, Mother, Guardian)
- Indian grading system (CGPA out of 10)
- Fee types common in Indian institutions
- Payment modes (UPI, NEFT, Cheque, DD, etc.)

## Tech Stack

- **Backend:** Django 5.2
- **Frontend:** Bootstrap 5.3, Bootstrap Icons
- **Database:** SQLite (default) / PostgreSQL
- **Charts:** Chart.js
- **Export:** OpenPyXL (Excel)
- **Forms:** Django Crispy Forms

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/student-management-system.git
cd student-management-system
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```

### 7. Access the Application
- **Main App:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/

## Default Credentials
- **Username:** admin
- **Password:** admin123

## Project Structure

```
student-management-system/
├── manage.py
├── requirements.txt
├── .gitignore
├── README.md
├── student_management/          # Django Project Settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── students/                    # Main Application
    ├── models.py               # Database Models
    ├── views.py                # View Functions
    ├── forms.py                # Django Forms
    ├── urls.py                 # URL Routing
    ├── admin.py                # Admin Configuration
    └── templates/
        └── students/
            ├── base.html
            ├── dashboard.html
            ├── student_list.html
            ├── student_detail.html
            ├── student_form.html
            ├── course_list.html
            ├── attendance_list.html
            ├── fee_list.html
            └── auth/
                ├── login.html
                └── signup.html
```

## Models

### Student
- Personal Info (Name, DOB, Gender, Blood Group)
- Identity (Aadhaar, Category, Religion)
- Address (Full Indian address with PIN)
- Family (Parents, Guardian, Income)
- Education (10th, 12th details)
- Academic (Department, Semester, CGPA)

### Course
- Code, Name, Department
- Credits, Semester, Instructor
- Max Students

### Enrollment
- Student-Course relationship
- Internal/External marks
- Indian grading (O, A+, A, B+, B, C, P, F)

### Attendance
- Present, Absent, Late, On Duty, Medical Leave

### Fee
- Multiple fee types (Tuition, Hostel, Mess, etc.)
- Payment modes (UPI, NEFT, Cheque, DD)
- Transaction tracking

## Screenshots

### Dashboard
- Total students, courses, departments
- GPA distribution chart
- Department-wise student count
- Recent admissions

### Student List
- Filterable by department, semester, status
- Sortable columns
- Pagination
- Export to Excel

### Student Form
- Comprehensive Indian student data entry
- Previous education details
- Family information

## License

MIT License

## Author

Built with Django
