from django.contrib import admin

from .models import BaseProduct, FavoriteProduct, UpdateReport
# Register your models here.

admin.site.register(BaseProduct)
admin.site.register(UpdateReport)

@admin.register(FavoriteProduct)
class BaseProductAdmin(admin.ModelAdmin):
    list_filter = ('user', 'saved_product')
