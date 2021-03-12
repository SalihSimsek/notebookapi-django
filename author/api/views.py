from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes

from author.models import Author

from .serializers import AuthorSerializer,CreateAuthorSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter,OrderingFilter


class ApiAuthorListView(ListAPIView):
    serializer_class = AuthorSerializer
    filter_backends = (SearchFilter,OrderingFilter)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    search_fields = ('firstname','lastname')

    def get_queryset(self):
        user = self.request.user.pk
        return Author.objects.filter(creator__pk=user)

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def get_author(request,pk):
    try:
        author = Author.objects.filter(creator__pk=request.user.pk,pk=pk)
    except Author.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    serializer = AuthorSerializer(author,many=True)
    return Response(serializer.data)

@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def create_author(request):
    if request.method == 'POST':
        data = request.data

        data['creator'] = request.user.pk
        serializer = CreateAuthorSerializer(data=data)

        data = {}

        if serializer.is_valid():
            author = serializer.save()
            data['firstname'] = author.firstname
            data['lastname'] = author.lastname
            data['creator'] = author.creator.pk
            data['response'] = 'Başarılı kayıt'
            return Response(data = data)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

#Yazar sil
@api_view(['DELETE',])
@permission_classes((IsAuthenticated,))
def delete_author(request,pk):
    try:
        author = Author.objects.get(pk=pk)
    except Author.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    user = request.user.pk
    creator = author.creator.pk
    data = {}
    if(user != creator):
        data['response'] = 'Yetki dışı işlem gerçekleştirildi'
        return Response(data)
    author.delete()
    data['response'] = '{} Idli Yazar Silindi'.format(pk)
    return Response(data)

#Yazar düzenle
@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def update_author(request,pk):
    try:
        author = Author.objects.get(pk=pk)
    except Author.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    data = {}
    user = request.user.pk
    creator = author.creator.pk
    if(user != creator):
        data['response'] = 'Yetki dışı işlem gerçekleştirildi'
        return Response(data)
    serializer = CreateAuthorSerializer(author,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        data['response'] = 'Güncellendi'
    return Response(data=data)