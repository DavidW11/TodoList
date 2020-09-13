from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from .models import Todo, Subtasks, Done


class TodoList(ListView):
    # todo add parameter for folder
    model = Todo

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        completed_list = Done.objects.all()
        completed_length = len(completed_list)
        context['completed_list'] = completed_list
        context['completed_length'] = completed_length
        return context


    def post(self, request):
        new = request.POST.get('new_event')
        event = Todo(event_text=new)
        event.save()
        return redirect(request.path)


class TaskDetail(View):

    def get(self, request, pk):
        main = Todo.objects.get(id=pk)
        subtask_list = Subtasks.objects.filter(main_task=main)
        context = {'subtask_list': subtask_list, 'main_task': main}
        return render(request, 'todo/todo_detail.html', context)

    def post(self, request, pk):
        main = Todo.objects.get(id=pk)
        subtask = request.POST.get('new_subtask')
        task = Subtasks(subtask_text=subtask, main_task=main)
        task.save()
        return redirect(request.path)


class UpdateTask(View):
    def get(self, request, pk):
        task = Todo.objects.get(id=pk)
        context = {'task': task}
        return render(request, 'todo/update_task.html', context)

    def post(self, request, pk):
        new_text = request.POST.get('new_task')
        Todo.objects.filter(id=pk).update(event_text=new_text)
        return redirect('todo:list')


class UpdateSubtask(View):
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


# need request argument, even though python highlighter does not know
def delete_task(request, event_id):
    main_task = Todo.objects.get(id=event_id)
    # todo foreign key
    finished_task = Done(done_text=main_task.event_text)
    finished_task.save()
    Todo.objects.filter(id=event_id).delete()
    return redirect('todo:list')


def delete_completed_task(request, completed_id):
    Done.objects.filter(id=completed_id).delete()
    return redirect('todo:list')


def delete_subtask(request, subtask_id):
    subtask = Subtasks.objects.get(id=subtask_id)
    main = Todo.objects.get(id=subtask.main_task.id)
    Subtasks.objects.filter(id=subtask_id).delete()
    return redirect('todo:detail', pk=main.id)


def add_description(request, pk):
    new_desc = request.POST.get('description')
    Todo.objects.filter(id=pk).update(description=new_desc)
    return redirect('todo:detail', pk=pk)


def clear_all(request):
    # todo
    Done.objects.all().delete()
    return redirect('todo:list')


def home_page(request):
    return redirect('todo:list')
