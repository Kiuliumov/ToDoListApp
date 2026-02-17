from rest_framework.serializers import ModelSerializer
from .models import Todo


class ToDoItemSerializer(ModelSerializer):

    class Meta:
        model = Todo
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')