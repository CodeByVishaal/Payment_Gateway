from django.contrib import admin
from .models import Products
# Register your models here.

class ProductsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image_preview', 'description', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('price',)
    readonly_fields = ('product_image',)

    def image_preview(self, obj):
        """Show image preview in admin panel."""
        if obj.product_image:
            return f'<img src="{obj.product_image.url}" width="50" height="50" style="border-radius: 5px;" />'
        return "No Image"

    image_preview.allow_tags = True
    image_preview.short_description = "Preview"

admin.site.register(Products, ProductsAdmin)