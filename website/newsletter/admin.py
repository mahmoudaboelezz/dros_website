from asyncio import format_helpers
from django.contrib import admin
from .models import Newsletter,QRCode
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

# Register your models here.
@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('name', 'email',)
    search_fields = ('name','email',)
    ordering = ('name', 'email', )

@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'event',)
    search_fields = ('user','event',)
    ordering = ('user', 'event', )
    readonly_fields = ('show_qr_code','verfication_code',)
    fieldsets = (
        (None, {
            'fields': ('user', 'event', 'show_qr_code', 'verfication_code','image','attend')
        }),
        
    )
    
    def show_qr_code(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="100" height="100" />')