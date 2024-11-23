from django.shortcuts import render, redirect
from django.http import HttpResponse
from todolist_app.models import TaskList
from todolist_app.forms import TaskForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required
def todolist(request):
  form = ''
  if request.method == "POST":
    form=TaskForm(request.POST or None)
    if form.is_valid():
      form.save(commit=False).manage=request.user
      form.save()
      messages.success(request, ("New task added!"))
      return redirect('todolist')
    else:
      messages.error(request, ("Form field has some error. Please correct it."))

  tasks_all = TaskList.objects.filter(manage=request.user)
  paginator = Paginator(tasks_all, 5)
  page = request.GET.get('page')
  tasks_all = paginator.get_page(page)
  return render(request, 'todolist.html', {'tasks_all': tasks_all, 'form': form})

@login_required
def delete_task(request, task_id):
  try:
    task=TaskList.objects.get(pk=task_id)
    if task.manage==request.user:
      task.delete()
      messages.success(request, ("Your task has been deleted successfully."))
    else:
      messages.error(request, ("Access restricted, You are not allowed to edit."))
  except ObjectDoesNotExist:
    messages.error(request, ("The requested task doesn't exist in the database."))
  return redirect('todolist')

@login_required
def edit_task(request, task_id):
  try:
    task_obj = TaskList.objects.get(pk=task_id)
    form=''
    if request.method == 'POST':
      form=TaskForm(request.POST or None, instance=task_obj)
      if form.is_valid():
        form.save()
        messages.success(request, ("Your task has been updated successfully."))
        return redirect("todolist")
      else:
        messages.error(request, ("Form field has some error. Please correct it."))

    return render(request, 'edit.html', {'task_obj': task_obj, 'form': form})
  except ObjectDoesNotExist:
    messages.error(request, ("The requested task doesn't exist in the database."))
    return redirect('todolist')

@login_required
def complete_task(request, task_id):
  try:
    task=TaskList.objects.get(pk=task_id)
    if task.manage==request.user:
      task.done = True
      task.save()
      messages.success(request, ("Your task has been successfuly marked as completed."))
    else:
      messages.error(request, ("Access restricted, You are not allowed to edit."))
  except ObjectDoesNotExist:
    messages.error(request, ("The requested task doesn't exist in the database."))
  return redirect('todolist')

@login_required
def pending_task(request, task_id):
  try:
    task=TaskList.objects.get(pk=task_id)
    if task.manage==request.user:
      task.done = False
      task.save()
      messages.success(request, ("Your task has been successfuly marked as pending."))
    else:
      messages.error(request, ("Access restricted, You are not allowed to edit."))
  except ObjectDoesNotExist:
    messages.error(request, ("The requested task doesn't exist in the database."))
  return redirect('todolist')

def index(request):
  context={
    "index_text": "Welcome to TaskMate!"
  }
  return render(request, 'index.html', context)

def about(request):
  context={
    "about_text": "Welcome to About Us Page"
  }
  return render(request, 'about.html', context)

def contact(request):
  context={
    "contact_text": "Welcome to Contact Us Page"
  }
  return render(request, 'contact.html', context)
