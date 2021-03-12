from django.urls import path
from .views import all_categories,get_category,create_category,update_category,delete_category

urlpatterns = [
    path('categories/',all_categories,name='all_categories'),
    path('create/',create_category,name='create_category'),
    path('<int:pk>/detail/',get_category,name='get_category'),
    path('<int:pk>/update/',update_category,name='update_category'),
    path('<int:pk>/delete/',delete_category,name='delete_category'),
]