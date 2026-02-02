from django.contrib import admin
from .models import Student, Course, Department, Enrollment, Attendance, Fee, Announcement


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'head', 'student_count', 'course_count')
    search_fields = ('name', 'code', 'head')
    ordering = ('name',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'department', 'credits', 'semester', 'instructor', 'is_active')
    list_filter = ('department', 'semester', 'is_active')
    search_fields = ('name', 'code', 'instructor')
    list_editable = ('is_active',)
    ordering = ('code',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'full_name', 'email', 'department', 'current_semester', 'cgpa', 'category', 'is_active')
    list_filter = ('is_active', 'gender', 'department', 'current_semester', 'category', 'state', 'is_hosteler')
    search_fields = ('first_name', 'last_name', 'email', 'student_id', 'aadhaar_number', 'phone')
    list_editable = ('is_active',)
    list_per_page = 20
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('student_id', 'first_name', 'last_name', 'email', 'phone', 
                      'date_of_birth', 'gender', 'blood_group')
        }),
        ('Indian Specific', {
            'fields': ('aadhaar_number', 'category', 'religion', 'nationality', 'mother_tongue')
        }),
        ('Address', {
            'fields': ('address', 'city', 'district', 'state', 'pincode'),
            'classes': ('collapse',)
        }),
        ('Family Information', {
            'fields': ('father_name', 'father_occupation', 'father_phone',
                      'mother_name', 'mother_occupation', 'mother_phone',
                      'guardian_name', 'guardian_phone', 'guardian_email', 'guardian_relation',
                      'annual_family_income'),
            'classes': ('collapse',)
        }),
        ('Previous Education - 10th', {
            'fields': ('tenth_board', 'tenth_school', 'tenth_year', 'tenth_percentage'),
            'classes': ('collapse',)
        }),
        ('Previous Education - 12th', {
            'fields': ('twelfth_board', 'twelfth_school', 'twelfth_year', 'twelfth_percentage', 'twelfth_stream'),
            'classes': ('collapse',)
        }),
        ('Academic Information', {
            'fields': ('department', 'admission_date', 'admission_type', 'roll_number',
                      'current_semester', 'cgpa', 'total_credits', 'is_active')
        }),
        ('Hostel', {
            'fields': ('is_hosteler', 'hostel_room'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('student_id', 'created_at', 'updated_at')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_date', 'grade', 'internal_marks', 'external_marks', 'is_active', 'completed')
    list_filter = ('is_active', 'completed', 'grade', 'course')
    search_fields = ('student__first_name', 'student__last_name', 'course__code')
    list_editable = ('grade', 'internal_marks', 'external_marks', 'is_active', 'completed')
    autocomplete_fields = ('student', 'course')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date', 'status', 'recorded_by')
    list_filter = ('status', 'date', 'course')
    search_fields = ('student__first_name', 'student__last_name', 'course__code')
    date_hierarchy = 'date'
    autocomplete_fields = ('student', 'course')


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('student', 'fee_type', 'amount', 'due_date', 'status', 'payment_mode', 'semester', 'academic_year')
    list_filter = ('status', 'fee_type', 'payment_mode', 'semester', 'academic_year')
    search_fields = ('student__first_name', 'student__last_name', 'student__student_id', 'receipt_number')
    list_editable = ('status',)
    date_hierarchy = 'due_date'


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'department', 'is_active', 'created_by', 'created_at')
    list_filter = ('priority', 'is_active', 'department')
    search_fields = ('title', 'content')
    list_editable = ('is_active',)
