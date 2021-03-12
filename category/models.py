from django.db import models
from account.models import Account
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=20,verbose_name='Category Name')
    creator = models.ForeignKey(Account,verbose_name="Creator",on_delete=models.CASCADE,related_name="creator_category")

    def __str__(self):
        return self.name