from django.db import models
class GoodsType(models.Model):
    type_name = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.type_name
# Create your models here.
class GoodsDetail(models.Model):

    goodname = models.CharField(max_length=200,null=True)
    goodprice = models.BigAutoField(null=True)    
    goodtype = models.ForeignKey(GoodsType, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<Goods: %s>" % self.goodname

    class Meta:
        ordering = ['-created_time']