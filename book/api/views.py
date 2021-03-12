from rest_framework.filters import SearchFilter, OrderingFilter 
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from rest_framework import status

# from store.pagination import CustomPagination

from .serializers import BookSerializer,CreateBookSerializer
from book.models import Book

##Case sensitive olayını kaldırmak için sıralanacak alanın değerleri
##küçük harfe çevrilmesini sağlayan metot.
from django.db.models.functions import Lower

class ApiBookListView(ListAPIView):
    serializer_class = BookSerializer
    filter_backends = (SearchFilter,OrderingFilter)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    # pagination_class = CustomPagination
    search_fields = ('bookname','author__firstname','author__lastname','quotation__text')

    def get_queryset(self):
        user = self.request.user.pk
        return Book.objects.filter(creator__pk=user)

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def get_book(request,pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data,status = status.HTTP_200_OK)
    return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)


@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def create_book(request):
    data = request.data

    data['creator'] = request.user.pk
    data['isRead'] = False
    data['isFavorite'] = False
    serializer = CreateBookSerializer(data=data)

    data = {}

    if serializer.is_valid():
        book = serializer.save()
        data['bookname'] = book.bookname
        data['creator'] = book.creator.pk
        data['page'] = book.page
        data['author'] = book.author.pk
        
        return Response(data=data,status=status.HTTP_200_OK)
    return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE',])
@permission_classes((IsAuthenticated,))
def delete_book(request,pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    user = request.user.pk
    creator = book.creator.pk
    data = {}
    if(user!=creator):
        data['response'] = 'Yetki dışı işlem gerçekleştirildi'
        return Response(data)
    book.delete()
    data['response'] = 'İşlem Başarılı'
    return Response(data=data,status = status.HTTP_200_OK)

@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def update_book(request,pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    user = request.user.pk
    creator = book.creator.pk

    data = {}
    if(user != creator):
        data['response'] = 'İşlem gerçekleştirilemedi. Yetki dışı alan.'
        return Response(data=data)

    if request.method == 'PUT':
        serializer = CreateBookSerializer(book,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            data['response'] = 'Güncellendi'
            return Response(data=data)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

