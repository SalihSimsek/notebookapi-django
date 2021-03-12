from django.urls import path
from .views import ApiQuotationListView,create_quotation,detail_quotation,delete_quotation,update_quotation

urlpatterns = [
    path('quotations/',ApiQuotationListView.as_view(),name='all_quotation'),
    path('create/',create_quotation,name='create_quotation'),
    path('<int:pk>/detail/',detail_quotation,name='detail_quotation'),
    path('<int:pk>/delete/',delete_quotation,name='delete_quotation'),
    path('<int:pk>/update/',update_quotation,name='update_quotation')
]