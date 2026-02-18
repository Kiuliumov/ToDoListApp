from django.urls import path
from .views import TodoListCreateView, TodoRetrieveDestroyView

urlpatterns = [
    path('', TodoListCreateView.as_view(), name='todo-list'),
    path('todos/<int:pk>/', TodoRetrieveDestroyView.as_view(), name='todo-detail'),
]