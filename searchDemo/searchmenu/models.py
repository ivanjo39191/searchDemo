from django.db import models

# Create your models here.

class GoodsType(models.Model):
    type_name = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.type_name


class GoodsDetail(models.Model):

    goodname = models.CharField(max_length=200,null=True)
    goodprice = models.BigIntegerField(null=True)
    goodshop = models.CharField(max_length=200,null=True)
    goodtype = models.ForeignKey(GoodsType, on_delete=models.CASCADE)
    goodlink = models.URLField(max_length=1000,null=True)
    goodimglink = models.URLField(max_length=1000,null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<Goods: %s>" % self.goodname

    class Meta:
        ordering = ['-created_time']