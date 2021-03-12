from django.db import models
from account.models import Account

from django.db.models.functions import Lower
# Create your models here.
class Author(models.Model):
    firstname = models.CharField(max_length=30,verbose_name='Firstname')
    lastname = models.CharField(max_length=30,verbose_name='Lastname')
    creator = models.ForeignKey(Account,verbose_name="Creator",on_delete=models.CASCADE,related_name="authors")

    def __str__(self):
        return self.firstname+" "+self.lastname

    class Meta:
        ordering = [Lower('firstname')]