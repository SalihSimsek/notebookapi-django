from account.models import Account
from rest_framework import serializers
from book.models import Book
from quotation.models import Quotation

class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = Account
        fields = ['email','username','password','password2']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def save(self):
        user = Account(
            email = self.validated_data['email'],
            username = self.validated_data['username'],
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password':'Password must match'})

        user.set_password(password)
        user.save()
        return user

class AccountSerializer(serializers.ModelSerializer):
    book_count = serializers.SerializerMethodField('get_book_count')
    favorited_book_count = serializers.SerializerMethodField('get_favorited_book')
    quotation_count = serializers.SerializerMethodField('get_notes_count')
    unread_count = serializers.SerializerMethodField('get_unread_count')
    class Meta:
        model = Account
        fields = ['pk','email','username','book_count','favorited_book_count','quotation_count','unread_count']

    def get_book_count(self,user):
        book_count = Book.objects.filter(creator__pk = user.pk).count()
        return book_count

    def get_favorited_book(self,user):
        fav_count = Book.objects.filter(creator__pk = user.pk, isFavorite = True).count()
        return fav_count

    def get_notes_count(self,user):
        quotation_count = Quotation.objects.filter(creator__pk = user.pk).count()
        return quotation_count

    def get_unread_count(self,user):
        unread_count = Book.objects.filter(creator__pk=user.pk, isRead =False).count()
        return unread_count

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)