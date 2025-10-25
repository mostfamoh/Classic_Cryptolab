from django.contrib import admin
from .models import CipherKey, EncryptionHistory


@admin.register(CipherKey)
class CipherKeyAdmin(admin.ModelAdmin):
    list_display = ('user', 'cipher_type', 'key_name', 'created_at')
    list_filter = ('cipher_type', 'created_at')
    search_fields = ('user__username', 'key_name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(EncryptionHistory)
class EncryptionHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'cipher_type', 'operation', 'mode', 'timestamp')
    list_filter = ('cipher_type', 'operation', 'mode', 'timestamp')
    search_fields = ('user__username', 'input_text', 'output_text')
    readonly_fields = ('timestamp',)
