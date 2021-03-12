from django.urls import path
from .views import ApiBookListView,get_book,create_book,delete_book,update_book


urlpatterns = [
    path('books/',ApiBookListView.as_view(),name='all_books'),
    path('create/',create_book,name='create_book'),
    path('<int:pk>/detail/',get_book,name='get_book'),
    path('<int:pk>/delete/',delete_book,name='delete_book'),
    path('<int:pk>/update/',update_book,name='update_book'),
]