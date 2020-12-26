from django.forms import ModelForm
from .models import Todo, Done, Subtasks

class AddTask(ModelForm):
    class Meta:
        model = Todo
        fields = ['event_text']
