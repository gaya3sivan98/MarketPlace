from rest_framework import serializers
from .models import Category, Service
from accounts.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image', 'icon']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']

class ServiceSerializer(serializers.ModelSerializer):
    provider = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = Service
        fields = ['id', 'provider', 'category', 'category_id', 'title', 'description', 'price', 'image', 'status', 'created_at', 'updated_at', 'is_active']
        read_only_fields = ['provider', 'created_at', 'updated_at', 'is_active']

    def create(self, validated_data):
        validated_data['provider'] = self.context['request'].user
        return super().create(validated_data)
