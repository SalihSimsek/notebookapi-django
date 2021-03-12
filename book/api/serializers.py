from book.models import Book
from rest_framework import serializers
from quotation.api.serializers import QuotationSerializer

class BookSerializer(serializers.ModelSerializer):
    author_firstname = serializers.SerializerMethodField('get_author_name')
    author_lastname = serializers.SerializerMethodField('get_author_lastname')
    quotation = QuotationSerializer('quotation',many=True)
    category = serializers.SerializerMethodField('get_category_name')
    class Meta:
        model = Book
        fields = ['id','bookname','page','isFavorite','isRead','category','author_firstname','author_lastname','quotation']

    def get_author_name(self,book):
        author = book.author.firstname
        return author

    def get_author_lastname(self,book):
        author = book.author.lastname
        return author

    def get_category_name(self,book):
        category = book.category.name
        return category



class CreateBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['bookname','page','category','author','creator','isFavorite','isRead']

