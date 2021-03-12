from rest_framework import serializers
from author.models import Author
from book.api.serializers import BookSerializer

class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer('books',many=True)

    class Meta:
        model = Author
        fields = ['id','firstname','lastname','books']

    

class CreateAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['firstname','lastname','creator']