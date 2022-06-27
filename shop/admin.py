from django.contrib import admin
from .models import Category, Product , Contact, Orders,CustomUser,Address,OrderProd
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import User
# Register your models here.

from django.utils.translation import gettext_lazy as _

class UserAdmin(DjangoUserAdmin):
    model = CustomUser
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name','address')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)





admin.site.register(CustomUser,UserAdmin)
admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Orders)
admin.site.register(Category)
admin.site.register(Address)
admin.site.register(OrderProd)
