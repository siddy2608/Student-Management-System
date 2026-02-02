from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Student, Course, Department, Enrollment, Attendance, Fee, Announcement


class SignUpForm(UserCreationForm):
    """User registration form."""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email address'
        })
    )
    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter first name'
        })
    )
    last_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter last name'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Create a password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email address is already registered.')
        return email


class StudentForm(forms.ModelForm):
    """Form for creating and updating Indian students."""
    
    class Meta:
        model = Student
        fields = [
            # Personal Info
            'first_name', 'last_name', 'email', 'phone',
            'date_of_birth', 'gender', 'blood_group',
            # Indian Specific
            'aadhaar_number', 'category', 'religion', 'nationality', 'mother_tongue',
            # Address
            'address', 'city', 'district', 'state', 'pincode',
            # Family Info
            'father_name', 'father_occupation', 'father_phone',
            'mother_name', 'mother_occupation', 'mother_phone',
            'guardian_name', 'guardian_phone', 'guardian_email', 'guardian_relation',
            'annual_family_income',
            # 10th Details
            'tenth_board', 'tenth_school', 'tenth_year', 'tenth_percentage',
            # 12th Details
            'twelfth_board', 'twelfth_school', 'twelfth_year', 'twelfth_percentage', 'twelfth_stream',
            # Academic
            'department', 'admission_type', 'current_semester', 'cgpa', 'roll_number',
            # Status
            'is_active', 'is_hosteler', 'hostel_room'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-digit mobile number'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'blood_group': forms.Select(attrs={'class': 'form-select'}),
            'aadhaar_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12-digit Aadhaar number', 'maxlength': '12'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'religion': forms.Select(attrs={'class': 'form-select'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_tongue': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Hindi, Tamil, Bengali'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-select'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '6-digit PIN code', 'maxlength': '6'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'father_occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'father_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-digit mobile'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '10-digit mobile'}),
            'guardian_name': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'guardian_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'guardian_relation': forms.TextInput(attrs={'class': 'form-control'}),
            'annual_family_income': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Annual income in ₹'}),
            'tenth_board': forms.Select(attrs={'class': 'form-select'}),
            'tenth_school': forms.TextInput(attrs={'class': 'form-control'}),
            'tenth_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2020'}),
            'tenth_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Percentage'}),
            'twelfth_board': forms.Select(attrs={'class': 'form-select'}),
            'twelfth_school': forms.TextInput(attrs={'class': 'form-control'}),
            'twelfth_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2022'}),
            'twelfth_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Percentage'}),
            'twelfth_stream': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Science/Commerce/Arts'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'admission_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'JEE/NEET/CET/Management'}),
            'current_semester': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 8}),
            'cgpa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '10'}),
            'roll_number': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_hosteler': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hostel_room': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Room number'}),
        }


class StudentFilterForm(forms.Form):
    """Form for filtering students."""
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Search students...'
    }))
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False,
        empty_label='All Departments',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    status = forms.ChoiceField(
        choices=[('', 'All Status'), ('active', 'Active'), ('inactive', 'Inactive')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    semester = forms.ChoiceField(
        choices=[('', 'All Semesters')] + [(i, f'Semester {i}') for i in range(1, 9)],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class CourseForm(forms.ModelForm):
    """Form for creating and updating courses."""
    
    class Meta:
        model = Course
        fields = [
            'name', 'code', 'department', 'description',
            'credits', 'semester', 'instructor', 'max_students', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course name'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., CS101'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'credits': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 6}),
            'semester': forms.Select(attrs={'class': 'form-select'}),
            'instructor': forms.TextInput(attrs={'class': 'form-control'}),
            'max_students': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class DepartmentForm(forms.ModelForm):
    """Form for creating and updating departments."""
    
    class Meta:
        model = Department
        fields = ['name', 'code', 'description', 'head']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department name'}),
            'code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., CS, ECE'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'head': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'HOD Name'}),
        }


class EnrollmentForm(forms.ModelForm):
    """Form for enrolling students in courses."""
    
    class Meta:
        model = Enrollment
        fields = ['student', 'course', 'grade', 'internal_marks', 'external_marks', 'is_active', 'completed']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'grade': forms.Select(attrs={'class': 'form-select'}),
            'internal_marks': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': 0, 'max': 40, 'placeholder': 'Out of 40'}),
            'external_marks': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': 0, 'max': 60, 'placeholder': 'Out of 60'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = Student.objects.filter(is_active=True)
        self.fields['course'].queryset = Course.objects.filter(is_active=True)


class AttendanceForm(forms.ModelForm):
    """Form for recording attendance."""
    
    class Meta:
        model = Attendance
        fields = ['student', 'course', 'date', 'status', 'remarks']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'remarks': forms.TextInput(attrs={'class': 'form-control'}),
        }


class BulkAttendanceForm(forms.Form):
    """Form for bulk attendance recording."""
    course = forms.ModelChoiceField(
        queryset=Course.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )


class FeeForm(forms.ModelForm):
    """Form for fee management (INR)."""
    
    class Meta:
        model = Fee
        fields = [
            'student', 'fee_type', 'amount', 'due_date', 
            'paid_date', 'paid_amount', 'payment_mode', 'transaction_id',
            'receipt_number', 'status', 'semester', 'academic_year', 'remarks'
        ]
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'fee_type': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': 0, 'placeholder': 'Amount in ₹'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'paid_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'paid_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': 0}),
            'payment_mode': forms.Select(attrs={'class': 'form-select'}),
            'transaction_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'UPI/NEFT Reference'}),
            'receipt_number': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'semester': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 8}),
            'academic_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '2025-2026'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class AnnouncementForm(forms.ModelForm):
    """Form for creating announcements."""
    
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'priority', 'department', 'is_active', 'expires_at']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'expires_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
