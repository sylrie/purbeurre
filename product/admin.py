from django.contrib import admin

from .models import SavedProduct, FavoriteProduct
# Register your models here.

admin.site.register(SavedProduct)

@admin.register(FavoriteProduct)
class SavedProductAdmin(admin.ModelAdmin):
    list_filter = ('user', 'saved_product')
