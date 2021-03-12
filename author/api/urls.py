from django.urls import path
from .views import ApiAuthorListView,create_author,delete_author,update_author,get_author

urlpatterns = [
    path('authors/',ApiAuthorListView.as_view(),name='all_authors'),
    path('create/',create_author,name='create_author'),
    path('<int:pk>/delete/',delete_author,name='delete_author'),
    path('<int:pk>/update/',update_author,name='update_author'),
    path('<int:pk>/detail/',get_author,name='get_author'),
]