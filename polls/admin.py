from django.contrib import admin

from polls.models import Students, SendMessagesLog


@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):
    """Админка User."""
    list_display = (
        'foreign_id',
        'name',
        'email',
        'phone',
        'status_id',
    )


@admin.register(SendMessagesLog)
class SendMessagesLogAdmin(admin.ModelAdmin):
    """Админка User."""
    list_display = (
        'student',
        'created_at',
        'is_message_send',
        'lessons_passed',
        'is_last_lesson_was_yesterday',
    )
    list_filter = (
        'created_at',
        'is_message_send',
        'lessons_passed',
        'is_last_lesson_was_yesterday',
    )
