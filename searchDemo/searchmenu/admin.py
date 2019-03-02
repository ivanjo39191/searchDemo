from django.contrib import admin
from .models import GoodsDetail, GoodsType
# Register your models here.
@admin.register(GoodsDetail)
class GoodsDetailAdmin(admin.ModelAdmin):
    list_display = ('id','goodname','goodprice','goodtype','goodshop','goodlink','goodimglink','created_time','last_updated_time')

@admin.register(GoodsType)
class GoodsTypeAdmin(admin.ModelAdmin):
    list_display = ('id','type_name')