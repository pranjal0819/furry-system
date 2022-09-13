from django.contrib import admin

from history.models import Category, Transaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'kind')
    list_display_links = ('__str__',)
    list_filter = ('kind',)
    ordering = ('kind', 'name')
    search_fields = ('name',)
    fieldsets = (
        (None, {'fields': ('name', 'kind')}),
        # ('Timestamp', {'classes': ('collapse',), 'fields': ('created_at', 'updated_at')}),
    )
    # readonly_fields = ('created_at', 'updated_at')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'kind', 'amount', 'category', 'account', 'user')
    list_display_links = ('__str__',)
    list_filter = ('account', 'category')
    search_fields = ('user',)
    fieldsets = (
        (None, {'fields': ('datetime', 'kind', 'category', 'amount', 'note')}),
        ('Account Details', {'fields': ('account', 'user')}),
        # ('Timestamp', {'classes': ('collapse',), 'fields': ('created_at', 'updated_at')}),
    )
    # readonly_fields = ('created_at', 'updated_at')
