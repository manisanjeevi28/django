from django.shortcuts import render, redirect
from django.contrib import messages
from users_app.models import CustomRegistrationForm

# Create your views here.
def register(request):

  if request.method == 'POST':
    form=CustomRegistrationForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, ("You have been successfully registered in the application. Please try login."))
      return redirect('register')
  else:
    form=CustomRegistrationForm()
  return render(request, 'register.html', {'form': form})
