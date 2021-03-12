from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from category.models import Category
from .serializers import CategorySerializer,CreateCategorySerializer

#get categories
@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def all_categories(request):
    user = request.user.pk
    categories = Category.objects.filter(creator__pk=user).order_by('name')
    serializer = CategorySerializer(categories,many=True)
    return Response(serializer.data)

#get category
@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def get_category(request,pk):
    try:
        category = Category.objects.filter(creator__pk=request.user.pk,pk=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CategorySerializer(category,many=True)
    return Response(serializer.data)

#create category
@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def create_category(request):
    data = request.data
    data['creator'] = request.user.pk
    serializer = CreateCategorySerializer(data=data)

    data = {}

    if serializer.is_valid():
        category = serializer.save()
        data['response'] = 'Kategori Oluşturuldu'
        return Response(data=data,status=status.HTTP_200_OK)
    return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

#update category
@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def update_category(request,pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    user = request.user.pk
    creator = book.creator.pk

    data={}

    if(user!=creator):
        data['response'] = 'İşlem gerçekleştirilemedi. Yetki dışı alan.'
        return Response(data=data)

    if request.method == 'PUT':
        serializer = CreateCategorySerializer(category,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            data['response'] = 'Güncellendi'
            return Response(data=data,status = status.HTTP_200_OK)
        return Response(status = status.HTTP_400_BAD_REQUEST)

#delete category
@api_view(['DELETE',])
@permission_classes((IsAuthenticated,))
def delete_category(request,pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user = request.user.pk
    creator = book.creator.pk

    data = {}
    
    if(user!=creator):
        data['response'] = 'Yetki dışı işlem gerçekleştirildi'
        return Response(data)
    category.delete()
    return Response(status=status.HTTP_200_OK)