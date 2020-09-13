from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.TodoList.as_view(), name='list'),
    path('delete/<int:event_id>', views.delete_task, name='delete'),
    path('subtask/<int:pk>', views.TaskDetail.as_view(), name='detail'),
    path('delete_subtask/<int:subtask_id>', views.delete_subtask, name='deletesub'),
    path('home_page/', views.home_page, name='home'),
    path('update_task/<int:pk>', views.UpdateTask.as_view(), name='updatetask'),
    path('update_subtask/<int:subtask_id>', views.UpdateSubtask.as_view(), name='updatesubtask'),
    path('add_desc/<int:pk>', views.add_description, name='adddesc'),
    path('delete_completed/<int:completed_id>', views.delete_completed_task, name='deletecompleted'),
    path('clear_all', views.clear_all, name='clearall'),

]
