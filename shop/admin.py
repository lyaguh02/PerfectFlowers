"""
Регистрация моделей в административной панели
"""
from django.contrib import admin
from shop.models import Category, Product, ViewCount


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ViewCount)
class ViewCountAdmin(admin.ModelAdmin):
    pass
