from django.contrib import admin
from .models import BookCategory,Book,BookImage,Author

# Register your models here.
class CategoryAdminPage(admin.ModelAdmin):
    search_fields=('category_title',)

class AuthorAdminPage(admin.ModelAdmin):
    search_fields=('author_name',)

class BookAdminPage(admin.ModelAdmin):
    ordering=['-id']
    list_display =['book_name','book_author','book_price','in_stock']
    search_fields=('book_name','book_author__author_name')

class BookImageAdminPage(admin.ModelAdmin):
    ordering=['-id']
    list_display =['image_of_book','is_default']
    search_fields=('image_of_book__book_name',)
    




admin.site.register(BookCategory,CategoryAdminPage)
admin.site.register(Book,BookAdminPage)
admin.site.register(BookImage,BookImageAdminPage)
admin.site.register(Author,AuthorAdminPage)
