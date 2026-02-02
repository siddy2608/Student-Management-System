from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from decimal import Decimal


class Department(models.Model):
    """Department/Faculty model."""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    head = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    @property
    def student_count(self):
        return self.students.count()
    
    @property
    def course_count(self):
        return self.courses.count()


class Course(models.Model):
    """Course model with detailed information."""
    SEMESTER_CHOICES = [
        (1, 'Semester 1'),
        (2, 'Semester 2'),
        (3, 'Semester 3'),
        (4, 'Semester 4'),
        (5, 'Semester 5'),
        (6, 'Semester 6'),
        (7, 'Semester 7'),
        (8, 'Semester 8'),
    ]
    
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    description = models.TextField(blank=True)
    credits = models.PositiveIntegerField(default=3, validators=[MinValueValidator(1), MaxValueValidator(6)])
    semester = models.PositiveIntegerField(choices=SEMESTER_CHOICES, default=1)
    instructor = models.CharField(max_length=100, blank=True)
    max_students = models.PositiveIntegerField(default=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['code']
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    @property
    def enrolled_count(self):
        return self.enrollments.filter(is_active=True).count()
    
    @property
    def available_seats(self):
        return self.max_students - self.enrolled_count


class Student(models.Model):
    """Enhanced Student model with relationships."""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]
    
    # Personal Information
    student_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    
    # Guardian Information
    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_phone = models.CharField(max_length=15, blank=True, null=True)
    guardian_email = models.EmailField(blank=True, null=True)
    guardian_relation = models.CharField(max_length=50, blank=True, null=True)
    
    # Academic Information
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='students')
    admission_date = models.DateField(default=timezone.now)
    current_semester = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(8)])
    gpa = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('4.00'))],
        default=Decimal('0.00')
    )
    total_credits = models.PositiveIntegerField(default=0)
    
    # Status
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
    
    def __str__(self):
        return f"{self.student_id} - {self.full_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        today = timezone.now().date()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
    
    @property
    def enrolled_courses(self):
        return self.enrollments.filter(is_active=True).count()
    
    @property
    def attendance_percentage(self):
        total = self.attendance_records.count()
        if total == 0:
            return 0
        present = self.attendance_records.filter(status='P').count()
        return round((present / total) * 100, 1)
    
    def save(self, *args, **kwargs):
        if not self.student_id:
            # Auto-generate student ID
            last_student = Student.objects.order_by('-id').first()
            if last_student:
                last_id = int(last_student.student_id[3:]) if last_student.student_id.startswith('STU') else 0
                self.student_id = f"STU{last_id + 1:05d}"
            else:
                self.student_id = "STU00001"
        super().save(*args, **kwargs)


class Enrollment(models.Model):
    """Student enrollment in courses."""
    GRADE_CHOICES = [
        ('A+', 'A+ (4.00)'), ('A', 'A (4.00)'), ('A-', 'A- (3.67)'),
        ('B+', 'B+ (3.33)'), ('B', 'B (3.00)'), ('B-', 'B- (2.67)'),
        ('C+', 'C+ (2.33)'), ('C', 'C (2.00)'), ('C-', 'C- (1.67)'),
        ('D+', 'D+ (1.33)'), ('D', 'D (1.00)'),
        ('F', 'F (0.00)'),
        ('W', 'Withdrawn'),
        ('I', 'Incomplete'),
    ]
    
    GRADE_POINTS = {
        'A+': 4.00, 'A': 4.00, 'A-': 3.67,
        'B+': 3.33, 'B': 3.00, 'B-': 2.67,
        'C+': 2.33, 'C': 2.00, 'C-': 1.67,
        'D+': 1.33, 'D': 1.00, 'F': 0.00,
    }
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_date = models.DateField(auto_now_add=True)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, blank=True, null=True)
    marks = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,
                                validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_active = models.BooleanField(default=True)
    completed = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['student', 'course']
        ordering = ['-enrolled_date']
    
    def __str__(self):
        return f"{self.student.full_name} - {self.course.code}"
    
    @property
    def grade_point(self):
        return self.GRADE_POINTS.get(self.grade, 0)


class Attendance(models.Model):
    """Attendance tracking for students."""
    STATUS_CHOICES = [
        ('P', 'Present'),
        ('A', 'Absent'),
        ('L', 'Late'),
        ('E', 'Excused'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    remarks = models.CharField(max_length=200, blank=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'course', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.student.full_name} - {self.course.code} - {self.date}"


class Fee(models.Model):
    """Fee management for students."""
    FEE_TYPE_CHOICES = [
        ('TUI', 'Tuition Fee'),
        ('LAB', 'Lab Fee'),
        ('LIB', 'Library Fee'),
        ('EXM', 'Exam Fee'),
        ('OTH', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('PEN', 'Pending'),
        ('PAI', 'Paid'),
        ('OVD', 'Overdue'),
        ('WAI', 'Waived'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fees')
    fee_type = models.CharField(max_length=3, choices=FEE_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='PEN')
    semester = models.PositiveIntegerField(default=1)
    academic_year = models.CharField(max_length=9, default='2025-2026')
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-due_date']
    
    def __str__(self):
        return f"{self.student.full_name} - {self.get_fee_type_display()} - {self.amount}"


class Announcement(models.Model):
    """Announcements for students."""
    PRIORITY_CHOICES = [
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
        ('U', 'Urgent'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='M')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='announcements', help_text='Leave blank for all departments')
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
