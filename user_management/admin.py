from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Student
from .forms import StudentSignUpForm

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False

# Add is_student
class UserInline(admin.StackedInline):
    model = User
    can_delete = False
    
# Define a new User admin

UserAdmin.inlines = (StudentInline, )
UserAdmin.list_display += ("is_student",)
UserAdmin.fieldsets +=  ((None, {'fields': ('is_student',)}), )

# Re-register UserAdmin
admin.site.register(User, UserAdmin)

