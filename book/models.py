from django.db import models
from author.models import Author
from category.models import Category
from account.models import Account

from django.db.models.functions import Lower
# Create your models here.
class Book(models.Model):
    bookname = models.CharField(max_length=100,verbose_name='Bookname')
    page = models.IntegerField(verbose_name='Page')
    isFavorite = models.BooleanField(verbose_name='Favorite',default=False)
    isRead = models.BooleanField(verbose_name='Read',default=False)
    author = models.ForeignKey(Author,verbose_name="Author",related_name='books',on_delete=models.CASCADE)
    category = models.ForeignKey(Category,verbose_name='Category',related_name='books',on_delete=models.CASCADE)
    creator = models.ForeignKey(Account,verbose_name="Creator",on_delete=models.CASCADE,related_name="creator_books")


    def __str__(self):
        return self.bookname

    class Meta:
        ordering = [Lower('bookname')]