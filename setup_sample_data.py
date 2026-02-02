"""
Script to create sample data for the Student Management System
Run with: python manage.py shell < setup_sample_data.py
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_management.settings')
django.setup()

from students.models import Department, Course, Student, Enrollment
from datetime import date, timedelta
from decimal import Decimal
import random

# Create Departments
departments_data = [
    {'code': 'CS', 'name': 'Computer Science', 'head': 'Dr. John Smith', 'description': 'Department of Computer Science and Engineering'},
    {'code': 'EE', 'name': 'Electrical Engineering', 'head': 'Dr. Sarah Johnson', 'description': 'Department of Electrical and Electronics Engineering'},
    {'code': 'ME', 'name': 'Mechanical Engineering', 'head': 'Dr. Michael Brown', 'description': 'Department of Mechanical Engineering'},
    {'code': 'CE', 'name': 'Civil Engineering', 'head': 'Dr. Emily Davis', 'description': 'Department of Civil Engineering'},
    {'code': 'BA', 'name': 'Business Administration', 'head': 'Dr. Robert Wilson', 'description': 'School of Business Administration'},
]

print("Creating departments...")
departments = {}
for dept_data in departments_data:
    dept, created = Department.objects.get_or_create(code=dept_data['code'], defaults=dept_data)
    departments[dept_data['code']] = dept
    print(f"  {'Created' if created else 'Exists'}: {dept.name}")

# Create Courses
courses_data = [
    {'code': 'CS101', 'name': 'Introduction to Programming', 'department': 'CS', 'credits': 3, 'semester': 1, 'instructor': 'Prof. Alan Turing'},
    {'code': 'CS201', 'name': 'Data Structures', 'department': 'CS', 'credits': 4, 'semester': 2, 'instructor': 'Prof. Ada Lovelace'},
    {'code': 'CS301', 'name': 'Database Systems', 'department': 'CS', 'credits': 3, 'semester': 3, 'instructor': 'Prof. Edgar Codd'},
    {'code': 'CS401', 'name': 'Machine Learning', 'department': 'CS', 'credits': 4, 'semester': 5, 'instructor': 'Prof. Andrew Ng'},
    {'code': 'EE101', 'name': 'Circuit Analysis', 'department': 'EE', 'credits': 4, 'semester': 1, 'instructor': 'Prof. Nikola Tesla'},
    {'code': 'EE201', 'name': 'Digital Electronics', 'department': 'EE', 'credits': 3, 'semester': 2, 'instructor': 'Prof. Claude Shannon'},
    {'code': 'ME101', 'name': 'Engineering Mechanics', 'department': 'ME', 'credits': 4, 'semester': 1, 'instructor': 'Prof. Isaac Newton'},
    {'code': 'BA101', 'name': 'Principles of Management', 'department': 'BA', 'credits': 3, 'semester': 1, 'instructor': 'Prof. Peter Drucker'},
]

print("\nCreating courses...")
courses = {}
for course_data in courses_data:
    dept_code = course_data.pop('department')
    course_data['department'] = departments[dept_code]
    course, created = Course.objects.get_or_create(code=course_data['code'], defaults=course_data)
    courses[course_data['code']] = course
    print(f"  {'Created' if created else 'Exists'}: {course.code} - {course.name}")

# Create Sample Students
first_names = ['James', 'Emma', 'Liam', 'Olivia', 'Noah', 'Ava', 'Oliver', 'Sophia', 'William', 'Isabella', 
               'Ethan', 'Mia', 'Alexander', 'Charlotte', 'Benjamin', 'Amelia', 'Lucas', 'Harper', 'Mason', 'Evelyn']
last_names = ['Anderson', 'Brown', 'Davis', 'Garcia', 'Johnson', 'Martinez', 'Miller', 'Moore', 'Smith', 'Taylor',
              'Thomas', 'Thompson', 'White', 'Williams', 'Wilson', 'Lee', 'Harris', 'Clark', 'Lewis', 'Robinson']

print("\nCreating students...")
students = []
dept_codes = list(departments.keys())

for i in range(15):
    first_name = first_names[i % len(first_names)]
    last_name = last_names[i % len(last_names)]
    email = f"{first_name.lower()}.{last_name.lower()}{i}@university.edu"
    
    dob = date(2000 + (i % 5), (i % 12) + 1, (i % 28) + 1)
    
    student_data = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'phone': f'+1-555-{100+i:03d}-{1000+i*7:04d}',
        'date_of_birth': dob,
        'gender': ['M', 'F', 'O'][i % 3],
        'department': departments[dept_codes[i % len(dept_codes)]],
        'current_semester': (i % 6) + 1,
        'gpa': Decimal(str(round(2.5 + (i % 15) * 0.1, 2))),
        'city': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'][i % 5],
        'state': ['NY', 'CA', 'IL', 'TX', 'AZ'][i % 5],
        'is_active': i % 10 != 0,
    }
    
    if not Student.objects.filter(email=email).exists():
        student = Student.objects.create(**student_data)
        students.append(student)
        print(f"  Created: {student.student_id} - {student.full_name}")
    else:
        student = Student.objects.get(email=email)
        students.append(student)
        print(f"  Exists: {student.student_id} - {student.full_name}")

# Create Enrollments
print("\nCreating enrollments...")
course_list = list(courses.values())
for student in students[:10]:
    num_courses = random.randint(2, 4)
    selected_courses = random.sample(course_list, min(num_courses, len(course_list)))
    
    for course in selected_courses:
        if not Enrollment.objects.filter(student=student, course=course).exists():
            grade = random.choice(['A', 'A-', 'B+', 'B', 'B-', 'C+', None])
            Enrollment.objects.create(
                student=student,
                course=course,
                grade=grade,
                marks=random.uniform(60, 95) if grade else None,
                is_active=True,
                completed=grade is not None
            )
            print(f"  Enrolled: {student.full_name} in {course.code}")

print("\n✓ Sample data created successfully!")
print(f"  - {Department.objects.count()} Departments")
print(f"  - {Course.objects.count()} Courses")
print(f"  - {Student.objects.count()} Students")
print(f"  - {Enrollment.objects.count()} Enrollments")
