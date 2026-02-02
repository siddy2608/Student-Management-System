from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
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
    max_students = models.PositiveIntegerField(default=60)
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
    """Enhanced Student model for Indian students."""
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
    
    CATEGORY_CHOICES = [
        ('GEN', 'General'),
        ('OBC', 'OBC (Other Backward Class)'),
        ('SC', 'SC (Scheduled Caste)'),
        ('ST', 'ST (Scheduled Tribe)'),
        ('EWS', 'EWS (Economically Weaker Section)'),
    ]
    
    RELIGION_CHOICES = [
        ('HIN', 'Hindu'),
        ('MUS', 'Muslim'),
        ('CHR', 'Christian'),
        ('SIK', 'Sikh'),
        ('BUD', 'Buddhist'),
        ('JAI', 'Jain'),
        ('OTH', 'Other'),
    ]
    
    STATE_CHOICES = [
        ('AN', 'Andaman and Nicobar Islands'),
        ('AP', 'Andhra Pradesh'),
        ('AR', 'Arunachal Pradesh'),
        ('AS', 'Assam'),
        ('BR', 'Bihar'),
        ('CH', 'Chandigarh'),
        ('CG', 'Chhattisgarh'),
        ('DN', 'Dadra and Nagar Haveli'),
        ('DD', 'Daman and Diu'),
        ('DL', 'Delhi'),
        ('GA', 'Goa'),
        ('GJ', 'Gujarat'),
        ('HR', 'Haryana'),
        ('HP', 'Himachal Pradesh'),
        ('JK', 'Jammu and Kashmir'),
        ('JH', 'Jharkhand'),
        ('KA', 'Karnataka'),
        ('KL', 'Kerala'),
        ('LA', 'Ladakh'),
        ('LD', 'Lakshadweep'),
        ('MP', 'Madhya Pradesh'),
        ('MH', 'Maharashtra'),
        ('MN', 'Manipur'),
        ('ML', 'Meghalaya'),
        ('MZ', 'Mizoram'),
        ('NL', 'Nagaland'),
        ('OD', 'Odisha'),
        ('PY', 'Puducherry'),
        ('PB', 'Punjab'),
        ('RJ', 'Rajasthan'),
        ('SK', 'Sikkim'),
        ('TN', 'Tamil Nadu'),
        ('TS', 'Telangana'),
        ('TR', 'Tripura'),
        ('UP', 'Uttar Pradesh'),
        ('UK', 'Uttarakhand'),
        ('WB', 'West Bengal'),
    ]
    
    BOARD_CHOICES = [
        ('CBSE', 'CBSE'),
        ('ICSE', 'ICSE'),
        ('STATE', 'State Board'),
        ('NIOS', 'NIOS'),
        ('IB', 'International Baccalaureate'),
        ('OTHER', 'Other'),
    ]
    
    # Validators
    aadhaar_validator = RegexValidator(
        regex=r'^\d{12}$',
        message='Aadhaar number must be 12 digits'
    )
    
    phone_validator = RegexValidator(
        regex=r'^[6-9]\d{9}$',
        message='Enter a valid 10-digit Indian mobile number'
    )
    
    pincode_validator = RegexValidator(
        regex=r'^\d{6}$',
        message='PIN code must be 6 digits'
    )
    
    # Personal Information
    student_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, validators=[phone_validator], blank=True, null=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True, null=True)
    
    # Indian Specific Fields
    aadhaar_number = models.CharField(max_length=12, validators=[aadhaar_validator], blank=True, null=True, unique=True)
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES, default='GEN')
    religion = models.CharField(max_length=3, choices=RELIGION_CHOICES, blank=True, null=True)
    nationality = models.CharField(max_length=50, default='Indian')
    mother_tongue = models.CharField(max_length=50, blank=True, null=True)
    
    # Address
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=2, choices=STATE_CHOICES, blank=True, null=True)
    pincode = models.CharField(max_length=6, validators=[pincode_validator], blank=True, null=True)
    
    # Parent/Guardian Information
    father_name = models.CharField(max_length=100, blank=True, null=True)
    father_occupation = models.CharField(max_length=100, blank=True, null=True)
    father_phone = models.CharField(max_length=10, validators=[phone_validator], blank=True, null=True)
    mother_name = models.CharField(max_length=100, blank=True, null=True)
    mother_occupation = models.CharField(max_length=100, blank=True, null=True)
    mother_phone = models.CharField(max_length=10, validators=[phone_validator], blank=True, null=True)
    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_phone = models.CharField(max_length=10, validators=[phone_validator], blank=True, null=True)
    guardian_email = models.EmailField(blank=True, null=True)
    guardian_relation = models.CharField(max_length=50, blank=True, null=True)
    annual_family_income = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, 
                                                help_text='Annual family income in INR')
    
    # Previous Education (10th)
    tenth_board = models.CharField(max_length=10, choices=BOARD_CHOICES, blank=True, null=True)
    tenth_school = models.CharField(max_length=200, blank=True, null=True)
    tenth_year = models.PositiveIntegerField(blank=True, null=True)
    tenth_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,
                                           validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    # Previous Education (12th)
    twelfth_board = models.CharField(max_length=10, choices=BOARD_CHOICES, blank=True, null=True)
    twelfth_school = models.CharField(max_length=200, blank=True, null=True)
    twelfth_year = models.PositiveIntegerField(blank=True, null=True)
    twelfth_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,
                                             validators=[MinValueValidator(0), MaxValueValidator(100)])
    twelfth_stream = models.CharField(max_length=50, blank=True, null=True, 
                                      help_text='Science/Commerce/Arts')
    
    # Academic Information
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='students')
    admission_date = models.DateField(default=timezone.now)
    admission_type = models.CharField(max_length=50, blank=True, null=True, 
                                      help_text='JEE/NEET/State CET/Management Quota/etc.')
    current_semester = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(8)])
    cgpa = models.DecimalField(
        max_digits=4, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('10.00'))],
        default=Decimal('0.00'),
        help_text='CGPA out of 10'
    )
    total_credits = models.PositiveIntegerField(default=0)
    roll_number = models.CharField(max_length=20, blank=True, null=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_hosteler = models.BooleanField(default=False)
    hostel_room = models.CharField(max_length=20, blank=True, null=True)
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
            # Auto-generate student ID (e.g., 2026CS001)
            year = timezone.now().year
            dept_code = self.department.code if self.department else 'GEN'
            last_student = Student.objects.filter(student_id__startswith=f"{year}{dept_code}").order_by('-id').first()
            if last_student:
                try:
                    last_num = int(last_student.student_id[-3:])
                    self.student_id = f"{year}{dept_code}{last_num + 1:03d}"
                except:
                    self.student_id = f"{year}{dept_code}001"
            else:
                self.student_id = f"{year}{dept_code}001"
        super().save(*args, **kwargs)


class Enrollment(models.Model):
    """Student enrollment in courses."""
    GRADE_CHOICES = [
        ('O', 'O (Outstanding) - 10'),
        ('A+', 'A+ (Excellent) - 9'),
        ('A', 'A (Very Good) - 8'),
        ('B+', 'B+ (Good) - 7'),
        ('B', 'B (Above Average) - 6'),
        ('C', 'C (Average) - 5'),
        ('P', 'P (Pass) - 4'),
        ('F', 'F (Fail) - 0'),
        ('AB', 'Absent'),
        ('W', 'Withdrawn'),
        ('I', 'Incomplete'),
    ]
    
    GRADE_POINTS = {
        'O': 10, 'A+': 9, 'A': 8, 'B+': 7, 'B': 6, 
        'C': 5, 'P': 4, 'F': 0,
    }
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_date = models.DateField(auto_now_add=True)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, blank=True, null=True)
    internal_marks = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,
                                         validators=[MinValueValidator(0), MaxValueValidator(40)],
                                         help_text='Internal/Assignment marks out of 40')
    external_marks = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True,
                                         validators=[MinValueValidator(0), MaxValueValidator(60)],
                                         help_text='External/Exam marks out of 60')
    is_active = models.BooleanField(default=True)
    completed = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['student', 'course']
        ordering = ['-enrolled_date']
    
    def __str__(self):
        return f"{self.student.full_name} - {self.course.code}"
    
    @property
    def total_marks(self):
        internal = self.internal_marks or 0
        external = self.external_marks or 0
        return internal + external
    
    @property
    def grade_point(self):
        return self.GRADE_POINTS.get(self.grade, 0)


class Attendance(models.Model):
    """Attendance tracking for students."""
    STATUS_CHOICES = [
        ('P', 'Present'),
        ('A', 'Absent'),
        ('L', 'Late'),
        ('OD', 'On Duty'),
        ('ML', 'Medical Leave'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='P')
    remarks = models.CharField(max_length=200, blank=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'course', 'date']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.student.full_name} - {self.course.code} - {self.date}"


class Fee(models.Model):
    """Fee management for students (Indian Rupees)."""
    FEE_TYPE_CHOICES = [
        ('TUI', 'Tuition Fee'),
        ('ADM', 'Admission Fee'),
        ('EXM', 'Examination Fee'),
        ('LAB', 'Laboratory Fee'),
        ('LIB', 'Library Fee'),
        ('HOS', 'Hostel Fee'),
        ('MES', 'Mess Fee'),
        ('TRA', 'Transport Fee'),
        ('SPO', 'Sports Fee'),
        ('DEV', 'Development Fee'),
        ('CAU', 'Caution Deposit'),
        ('OTH', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('PEN', 'Pending'),
        ('PAI', 'Paid'),
        ('OVD', 'Overdue'),
        ('PAR', 'Partially Paid'),
        ('WAI', 'Waived'),
    ]
    
    PAYMENT_MODE_CHOICES = [
        ('CASH', 'Cash'),
        ('UPI', 'UPI'),
        ('NEFT', 'NEFT/RTGS'),
        ('CHQ', 'Cheque'),
        ('DD', 'Demand Draft'),
        ('CARD', 'Credit/Debit Card'),
        ('ONL', 'Online Payment'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fees')
    fee_type = models.CharField(max_length=3, choices=FEE_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text='Amount in INR')
    due_date = models.DateField()
    paid_date = models.DateField(blank=True, null=True)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_mode = models.CharField(max_length=4, choices=PAYMENT_MODE_CHOICES, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    receipt_number = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='PEN')
    semester = models.PositiveIntegerField(default=1)
    academic_year = models.CharField(max_length=9, default='2025-2026')
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-due_date']
    
    def __str__(self):
        return f"{self.student.full_name} - {self.get_fee_type_display()} - ₹{self.amount}"
    
    @property
    def balance_amount(self):
        return self.amount - self.paid_amount


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
