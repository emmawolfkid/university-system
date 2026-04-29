from django.contrib import admin
from .models import User, StudentProfile, InstructorProfile, StaffProfile

admin.site.register(User)
admin.site.register(StudentProfile)
admin.site.register(InstructorProfile)
admin.site.register(StaffProfile)