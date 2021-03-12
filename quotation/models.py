from django.db import models
from book.models import Book
from account.models import Account

from django.db.models.functions import Lower
# Create your models here.

class Quotation(models.Model):
    text = models.TextField(verbose_name="Text")
    quoted_book = models.ForeignKey(Book,verbose_name="Quoted Book",related_name="quotation",on_delete=models.CASCADE)
    found_page = models.IntegerField(verbose_name="Page Number")
    creator = models.ForeignKey(Account,verbose_name="Creator",on_delete=models.CASCADE,related_name="creator_quotations")


    def __str__(self):
        return self.text

    class Meta:
        ordering = [Lower('text')]