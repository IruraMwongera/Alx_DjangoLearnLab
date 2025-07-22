from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Book, Author, Library, Librarian, CustomUser, UserProfile

# Custom UserAdmin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'date_joined', 'is_staff']
    search_fields = ('username', 'email')
    ordering = ('username',)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )

# Register CustomUser
admin.site.register(CustomUser, CustomUserAdmin)

# Register other models
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')
    list_filter = ('publication_year',)

admin.site.register(Author)
admin.site.register(Library)
admin.site.register(Librarian)
admin.site.register(UserProfile)
