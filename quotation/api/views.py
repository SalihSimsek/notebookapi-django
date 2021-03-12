from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated

from quotation.models import Quotation

from .serializers import QuotationSerializer,CreateQuotationSerializer

from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
# from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter,OrderingFilter


class ApiQuotationListView(ListAPIView):
    serializer_class = QuotationSerializer
    filter_backends = (SearchFilter,OrderingFilter)
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    # pagination_class = PageNumberPagination
    search_fields = ('text','quoted_book__bookname',)

    def get_queryset(self):
        user = self.request.user.pk
        return Quotation.objects.filter(creator__pk=user)

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def detail_quotation(request,pk):
    try:
        quotation = Quotation.objects.get(pk=pk)
    except Quotation.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    serializer = QuotationSerializer(quotation)
    return Response(serializer.data,status = status.HTTP_200_OK)

#Create
@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def create_quotation(request):
    data = request.data
    data['creator'] = request.user.pk
    serializer = CreateQuotationSerializer(data=data)
    data= {}
    if serializer.is_valid():
        quotation = serializer.save()
        data['response'] = quotation.text 
        data['response'] = 'Created'
        return Response(data = data,status = status.HTTP_200_OK)
    return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

#Put
@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def update_quotation(request,pk):
    try:
        quotation = Quotation.objects.get(pk=pk)
    except Quotation.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    data = {}
    user = request.user.pk
    creator = quotation.creator.pk

    if(user!=creator):
        data['response'] = 'Yetki Dışı işlem gerçekleştirildi'
        return Response(data=data)

    serializer = CreateQuotationSerializer(quotation,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        data['response'] = 'Güncellendi'
        return Response(data=data,status=status.HTTP_200_OK)
    return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

#Delete
@api_view(['DELETE',])
@permission_classes((IsAuthenticated,))
def delete_quotation(request,pk):
    try:
        quotation = Quotation.objects.get(pk=pk)
    except Quotation.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    data = {}
    user = request.user.pk
    creator = quotation.creator.pk

    if(user!=creator):
        data['response'] = 'Yetki dışı işlem gerçekleştirildi'
        return Response(data=data)

    quotation.delete()
    data['response'] = 'Deleted'
    return Response(data=data,status = status.HTTP_200_OK)
