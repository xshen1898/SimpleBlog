from django.contrib import admin

from .models import Article, Category, Tag

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'category', 'author', 'publish_date']
    search_fields = ['title', 'content', 'category__name']

    def save_model(self, request, obj, form, change):
        obj.author = request.user.username
        obj.save()


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(Tag)
