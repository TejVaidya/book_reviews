from django.contrib import admin
from .models import User, Book, Review

class UserAdmin(admin.ModelAdmin):
    search_fields=('name', 'email')
    list_display = ('name', 'email')
    
admin.site.register(User,UserAdmin)

class BookAdmin(admin.ModelAdmin):
    search_fields=('title','author','genre')
    list_display = ('title','author','genre', 'summary')

admin.site.register(Book,BookAdmin)

class ReviewAdmin(admin.ModelAdmin):
    search_fields=('rating',)
    list_display = ('book_name', 'reviewer_name', 'rating', 'comment', 'created_at')

    def book_name(self,obj:Book):
        return obj.book.title
    
    def reviewer_name(self,obj:User):
        return obj.user.name
    
admin.site.register(Review,ReviewAdmin)

