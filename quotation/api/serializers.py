from rest_framework import serializers
from quotation.models import Quotation

class QuotationSerializer(serializers.ModelSerializer):
    quoted_book = serializers.SerializerMethodField('get_book_name')
    class Meta:
        model = Quotation
        fields = ['pk','text','quoted_book','found_page','creator']

    def get_book_name(self,quotation):
        book = quotation.quoted_book.bookname
        return book

    


class CreateQuotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotation
        fields = ['text','quoted_book','found_page','creator']