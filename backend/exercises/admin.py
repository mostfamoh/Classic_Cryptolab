from django.contrib import admin
from .models import Exercise, Submission, ActivityLog


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'cipher_type', 'difficulty', 'points', 'is_active', 'due_date')
    list_filter = ('cipher_type', 'difficulty', 'is_active', 'created_at')
    search_fields = ('title', 'description', 'instructor__username')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Info', {
            'fields': ('instructor', 'title', 'description', 'cipher_type', 'difficulty')
        }),
        ('Exercise Content', {
            'fields': ('ciphertext', 'correct_answer', 'hints', 'points')
        }),
        ('Status', {
            'fields': ('is_active', 'due_date')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'exercise', 'status', 'score', 'submitted_at', 'graded_at')
    list_filter = ('status', 'submitted_at', 'graded_at')
    search_fields = ('student__username', 'exercise__title', 'answer')
    readonly_fields = ('submitted_at', 'graded_at')


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'timestamp', 'ip_address')
    list_filter = ('activity_type', 'timestamp')
    search_fields = ('user__username',)
    readonly_fields = ('timestamp',)
