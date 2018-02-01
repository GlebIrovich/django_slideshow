#user_management/views

from django.contrib.auth import login
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import CreateView

from .forms import StudentSignUpForm
from .models import User

class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('carousel:list_classes')
    
    def form_invalid(self, form):
        return render(
                    self.request, 'registration/signup_form.html',
                    {'form': form}
                    )

