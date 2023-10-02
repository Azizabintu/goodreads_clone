from django.contrib import admin
from books.models import Book,Book_Author,Review,Author

# Register your models here.

class BookAdmin(admin.ModelAdmin):
    search_fields = ('title','isbn')
    list_display = ('title','isbn','description')

class AuthorAdmin(admin.ModelAdmin):
    pass

class BookAuthorAdmin(admin.ModelAdmin):
    list_filter = ('book','author')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user','book','comment','stars_given')
    list_filter = ('stars_given',)

admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book_Author, BookAuthorAdmin)
admin.site.register(Review, ReviewAdmin)