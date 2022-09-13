from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from account.models import Account, Liability

admin.site.unregister(get_user_model())


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'kind', 'balance', 'hidden', 'user')
    list_display_links = ('__str__',)
    list_filter = ('kind', 'hidden')
    search_fields = ('user',)
    fieldsets = (
        (None, {'fields': ('name', 'hidden', 'kind', 'balance')}),
        ('Account Details', {'fields': ('settings', 'user')}),
        # ('Timestamp', {'classes': ('collapse',), 'fields': ('created_at', 'updated_at')}),
    )
    # readonly_fields = ('created_at', 'updated_at')


@admin.register(Liability)
class LiabilityAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'credit', 'debit', 'account', 'user')
    list_display_links = ('__str__',)
    list_filter = ('account',)
    search_fields = ('user',)
    fieldsets = (
        (None, {'fields': ('reference_type', 'reference_id', 'credit', 'debit')}),
        ('Account Details', {'fields': ('account', 'user')}),
        # ('Timestamp', {'classes': ('collapse',), 'fields': ('created_at', 'updated_at')}),
    )
    # readonly_fields = ('created_at', 'updated_at')


@admin.register(get_user_model())
class UserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')
    list_display_links = ('username', 'email')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        (
            'Permissions',
            {
                'classes': ('collapse',),
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {'classes': ('wide',), 'fields': ('username', 'email', 'password1', 'password2')},
        ),
    )
    readonly_fields = ('date_joined',)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(admin.ModelAdmin, self).get_readonly_fields(request, obj)
        if not request.user.is_superuser:
            readonly_fields += ('is_staff', 'is_superuser')

            if not obj:
                return readonly_fields

            if obj.is_superuser or (obj.is_staff and request.user.pk != obj.pk):
                readonly_fields += ('username', 'password', 'email', 'is_active', 'groups')

        return readonly_fields
