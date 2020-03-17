from django.contrib import admin

from .models import Products, FavoriteProduct, UpdateReport
# Register your models here.

admin.site.register(Products)
admin.site.register(UpdateReport)

@admin.register(FavoriteProduct)
class ProductsAdmin(admin.ModelAdmin):
    list_filter = ('user', 'saved_product')
