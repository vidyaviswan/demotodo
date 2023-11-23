from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.detail import  DetailView
from django.views.generic.edit import UpdateView, DeleteView
from todoapp.forms import todoform
from todoapp.models import Task

class Tasklistview(ListView):
    model = Task
    template_name = 'home.html'
    context_object_name = 'task1'

class Taskdetailview(DetailView):
    model = Task
    template_name = 'details.html'
    context_object_name = 'task'

class Taskupdatelview(UpdateView):
    model = Task
    template_name = 'update1.html'
    context_object_name = 'task'
    fields = ('name','priority','date')

    def get_success_url(self):
        return reverse_lazy('cbvdetail',kwargs={'pk':self.object.id})

class Taskdeleteview(DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url =reverse_lazy ('cbvhome')

def home(request):
    task = Task.objects.all()
    if request.method=='POST':
        name=request.POST.get('name','')
        priority = request.POST.get('priority','')
        date = request.POST.get('date', '')
        task1 = Task(name=name, priority=priority,date=date)
        task1.save()
        #messages.info(request, "Data Added Successfully.....")


    return render(request,'home.html',{'task1':task})


def delete(request,taskid):
    task=Task.objects.get(id=taskid)
    if request.method =='POST':
        task.delete()
        return redirect('/')
    return render(request,'delete.html')

def update(request,id):
    task=Task.objects.get(id=id)
    f=todoform(request.POST or None, instance=task)
    if f.is_valid():
        f.save()
        return redirect('/')
    return render(request, 'update.html', {'f': f,'task':task})
