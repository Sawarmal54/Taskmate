from django.shortcuts import render,redirect
from todolist.models import TaskList
from todolist.forms import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required
def todolist(request):
    if request.method == "POST":
        form = TaskForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.manage = request.user
            instance.save()
        messages.success(request,('New Task Added!'))
        return redirect('todolist')
    else:
        all_tasks = TaskList.objects.filter(manage=request.user).order_by('creation_date')
        paginator = Paginator(all_tasks,5)
        page = request.GET.get('pg')
        all_tasks=paginator.get_page(page)
        context={
            'todo': all_tasks,
        }
        return render(request,"todolist.html",context)

def contact(request):
    context={
        'contact_text':"welcome to contact page",
    }
    return render(request,"contact.html",context)


def about(request):
    context={
        'about_text':"welcome to about Page",
    }
    return render(request,"about.html",context)

@login_required
def delete_task(request, task_id):
    task=TaskList.objects.get(pk=task_id)
    if task.manage == request.user:
        task.delete()
    else:
        messages.error(request,("Access Restricted! You are not allowed "))
        
    return redirect('todolist')

@login_required
def edit_task(request,task_id):
    if request.method == "POST":
        task = TaskList.objects.get(pk=task_id)
        form = TaskForm(request.POST or None, instance=task)
        if form.is_valid:
            form.save()
            
        messages.success(request,(' Task Edited!'))
        return redirect('todolist')
    else:
        task_obj = TaskList.objects.get(pk=task_id)
        return render(request,"edit.html",{'todo': task_obj,})

@login_required
def complete(request,task_id):
    task=TaskList.objects.get(pk=task_id)
    if task.manage == request.user:
        if task.done == True:
            task.done=False
            task.save()
            return redirect('todolist')
        else:
            task.done=True
            task.save()
    else:
        messages.error(request,("Access Restricted! You are not allowed "))
    return redirect('todolist')


def index(request):
    context={
        'home_text':"welcome to Home page",
    }
    return render(request,"index.html",context)
