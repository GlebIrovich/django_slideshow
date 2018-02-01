#user_management/forms

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Student, User

class StudentSignUpForm(UserCreationForm):
    student_id = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=100)
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    class Meta(UserCreationForm.Meta):
        model = User

    # verify uniqeuness
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email= email).exists():
            raise forms.ValidationError('This email is already used for registration.')
        return email
    def clean_student_id(self):
        student_id = self.cleaned_data['student_id']
        if Student.objects.filter(student_id= student_id).exists():
            raise forms.ValidationError('This student ID is already used for registration.')
        return student_id

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.email = self.cleaned_data.get('email')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.save()
        student = Student.objects.create(user=user)
        student.student_id = self.cleaned_data.get('student_id')
        student.save()
        return user