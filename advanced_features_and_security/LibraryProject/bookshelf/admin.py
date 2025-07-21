from django.contrib import admin
from .models import Book, CustomUser  # ✅ Import both Book and CustomUser
from django.contrib.auth.admin import UserAdmin  # ✅ Use Django's built-in UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Optional: Customize the admin display
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('date_of_birth', 'profile_photo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('date_of_birth', 'profile_photo')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)  # ✅ Register the custom user

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')
    list_filter = ('publication_year',)
