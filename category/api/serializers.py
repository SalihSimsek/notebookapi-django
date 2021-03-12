from rest_framework import serializers
from category.models import Category
from book.api.serializers import BookSerializer
class CategorySerializer(serializers.ModelSerializer):
    books = BookSerializer('books',many=True)
    class Meta:
        model = Category
        fields = ['id','name','books']

class CreateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name','creator']