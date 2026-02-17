from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Todo

User = get_user_model()


class BaseTodoTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="StrongPass123!"
        )

        self.other_user = User.objects.create_user(
            username="otheruser",
            password="StrongPass123!"
        )

        response = self.client.post(reverse('token_obtain_pair'), {
            "username": "testuser",
            "password": "StrongPass123!"
        })

        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.todo1 = Todo.objects.create(
            user=self.user,
            title="First Todo",
            description="Test description",
            completed=False
        )

        self.todo2 = Todo.objects.create(
            user=self.user,
            title="Completed Task",
            description="Done",
            completed=True
        )

        self.other_todo = Todo.objects.create(
            user=self.other_user,
            title="Other User Todo",
            completed=False
        )


class TodoCreateTest(BaseTodoTest):

    def test_create_todo(self):
        response = self.client.post(reverse('todo-list'), {
            "title": "New Task",
            "description": "Testing create"
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todo.objects.filter(user=self.user).count(), 3)


class TodoListTest(BaseTodoTest):

    def test_list_only_user_todos(self):
        response = self.client.get(reverse('todo-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # should exclude other user's todo


class TodoRetrieveTest(BaseTodoTest):

    def test_retrieve_single_todo(self):
        url = reverse('todo-detail', args=[self.todo1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "First Todo")


class TodoDeleteTest(BaseTodoTest):

    def test_delete_todo(self):
        url = reverse('todo-detail', args=[self.todo1.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Todo.objects.filter(id=self.todo1.id).exists())


class TodoFilterTest(BaseTodoTest):

    def test_filter_completed(self):
        response = self.client.get(reverse('todo-list') + '?completed=true')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertTrue(response.data[0]['completed'])


class TodoSearchTest(BaseTodoTest):

    def test_search_by_title(self):
        response = self.client.get(reverse('todo-list') + '?search=Completed')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Completed Task")


class TodoOrderingTest(BaseTodoTest):

    def test_ordering_desc(self):
        response = self.client.get(reverse('todo-list') + '?ordering=-created_at')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], "Completed Task")


class TodoSecurityTest(BaseTodoTest):

    def test_cannot_access_other_users_todo(self):
        url = reverse('todo-detail', args=[self.other_todo.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TodoAuthTest(APITestCase):

    def test_authentication_required(self):
        response = self.client.get(reverse('todo-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)