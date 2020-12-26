from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from .models import Todo, Subtasks, Done
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AddTask
from django.urls import reverse_lazy

'''
class TodoList(LoginRequiredMixin, View):

    def get(self, request):
        user = User.objects.get(username=request.user.username)
        completed_list = Done.objects.filter(username=user)
        completed_length = len(completed_list)
        object_list = Todo.objects.filter(username=user)
        form = AddTask()
        context = {'completed_list':completed_list, 'completed_length':completed_length,
                   'object_list':object_list, 'form':form}
        return render(request, 'todo/todo_list.html', context)

    def post(self, request):
        user = User.objects.get(username=request.user.username)
        form = AddTask(request.POST)
        if not form.is_valid():
            context = {'form':form}
            return render(request, self.template, context)
        task = form.save(commit=False)
        task.username=user
        task.save()
        return redirect(request.path)
'''

class TodoList(LoginRequiredMixin, CreateView):

    template_name = 'todo/todo_list.html'
    model = Todo
    fields = ['event_text']
    success_url = reverse_lazy('todo:list')

    def get_context_data(self, **kwargs):
        user = User.objects.get(username=self.request.user.username)
        object_list = Todo.objects.filter(username=user)
        context = super(TodoList, self).get_context_data(**kwargs)
        context['object_list'] = object_list
        return context

    def form_valid(self, form):
        object = form.save(commit=False)
        object.username = self.request.user
        object.save()
        return super(TodoList, self).form_valid(form)


'''
class TaskDetail(LoginRequiredMixin, View):
    def get(self, request, pk):
        main=Todo.objects.get(id=pk)
        subtask_list=Subtasks.objects.filter(main_task=main)
        context={'subtask_list': subtask_list, 'main_task': main}
        return render(request, 'todo/todo_detail.html', context)

    def post(self, request, pk):
        main=Todo.objects.get(id=pk)
        subtask=request.POST.get('new_subtask')
        task=Subtasks(subtask_text=subtask, main_task=main)
        task.save()
        return redirect(request.path)
'''

# todo how to get pk parameter
class TaskDetail(LoginRequiredMixin, View):

    template_name = 'todo/todo_detail.html'
    model = Subtasks
    fields = ['subtask_text']

    # def dispatch(self, request, *args, **kwargs):

    def get_context_data(self, **kwargs):
        self.pk = kwargs.get('pk')
        context = super(TaskDetail, self).get_context_data(**kwargs)
        main_task = Todo.objects.get(id=self.pk)
        context['main_task'] = main_task
        context['subtask_list'] = Subtasks.objects.filter(main_task = main_task)
        return context

    def form_valid(self, form, **kwargs):
        #pk = kwargs.get('pk')
        object = form.save(commit=False)
        object.main_task = Todo.objects.get(id=self.pk)
        object.save()
        return super(TaskDetail, self).form_valid(form)


'''
class UpdateTask(LoginRequiredMixin, View):
    def get(self, request, pk):
        task = Todo.objects.get(id=pk)
        context = {'task': task}
        return render(request, 'todo/update_task.html', context)

    def post(self, request, pk):
        new_text = request.POST.get('new_task')
        Todo.objects.filter(id=pk).update(event_text=new_text)
        return redirect('todo:list')
'''


class UpdateTask(LoginRequiredMixin, UpdateView):

    template_name='todo/update_task.html'
    model=Todo
    fields=['event_text']
    success_url=reverse_lazy('todo:list')


'''
class UpdateSubtask(LoginRequiredMixin, View):
    # todo django update view
    def get(self, request, subtask_id):
        subtask = Subtasks.objects.get(id=subtask_id)
        main = Todo.objects.get(id=subtask.main_task.id)
        context = {'task': subtask, 'main_task':main}
        return render(request, 'todo/update_subtask.html', context)

    def post(self, request, subtask_id):
        new_text = request.POST.get('new_task')
        Subtasks.objects.filter(id=subtask_id).update(subtask_text=new_text)
        subtask = Subtasks.objects.get(id=subtask_id)
        main = Todo.objects.get(id=subtask.main_task.id)
        return redirect('todo:detail', pk=main.id)
'''


class UpdateSubtask(LoginRequiredMixin, UpdateView):

    template_name='todo/update_subtask.html'
    model=Subtasks
    fields=['subtask_text']

    def get_context_data(self, **kwargs):
        context = super(UpdateSubtask, self).get_context_data(**kwargs)
        context['main_task'] = self.object.main_task
        return context

    def get_success_url(self):
        main_task = self.object.main_task
        return reverse_lazy('todo:detail', args=(main_task.id,))


# need request argument, even though python highlighter does not know
def delete_task(request, event_id):
    #main_task = Todo.objects.get(id=event_id)
    #finished_task = Done(done_text=main_task.event_text)
    #finished_task.save()
    Todo.objects.filter(id=event_id).delete()
    return redirect('todo:list')

def delete_subtask(request, subtask_id):
    main_task = Subtasks.objects.get(id=subtask_id).main_task
    Subtasks.objects.filter(id=subtask_id).delete()
    return redirect('todo:detail', pk=main_task.id)


def add_description(request, pk):
    new_desc = request.POST.get('description')
    Todo.objects.filter(id=pk).update(description=new_desc)
    return redirect('todo:detail', pk=pk)


'''
def delete_completed_task(request, completed_id):
    Done.objects.filter(id=completed_id).delete()
    return redirect('todo:list')

def clear_all(request):
    # todo user only
    Done.objects.all().delete()
    #Done.objects.filter(username=request.user.username).delete()
    return redirect('todo:list')
'''

def home_page(request):
    return redirect('todo:list')
