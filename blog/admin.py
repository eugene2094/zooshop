from django.contrib import admin
from django.utils.html import format_html
from .models import Post, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'title', 'author', 'category', 'published', 'created_at')
    list_filter = ('published', 'created_at', 'category')
    search_fields = ('title', 'content', 'excerpt')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('published',)
    ordering = ('-created_at',)

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" style="object-fit:cover;border-radius:4px;" />', obj.image.url)
        return "-"
    thumbnail.short_description = "Мініатюра"

