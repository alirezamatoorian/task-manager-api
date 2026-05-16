from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()


# Register your models here.

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('phone',)
    list_filter = ('is_active',)
    search_fields = ('phone',)
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('phone', 'password',"email","first_name","last_name")}),
        ('دسترسی‌ها', {'fields': ('is_active', 'is_superuser',"is_staff", 'groups', 'user_permissions')}),
        ('تاریخ‌ها', {'fields': ('last_login',"date_joined")}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password', 'is_active')}
         ),
    )
    readonly_fields = ('date_joined',)


admin.site.register(User, UserAdmin)