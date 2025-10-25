from django.contrib import admin
from .models import AttackLog


@admin.register(AttackLog)
class AttackLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'cipher_type', 'attack_type', 'success', 'timestamp')
    list_filter = ('cipher_type', 'attack_type', 'success', 'timestamp')
    search_fields = ('user__username', 'target_text')
    readonly_fields = ('timestamp',)
