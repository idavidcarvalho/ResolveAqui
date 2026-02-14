from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'ticket', 'text_preview', 'created_at')
    list_filter = ('created_at', 'ticket__status')
    search_fields = ('text', 'author__email', 'ticket__problem__name')
    readonly_fields = ('created_at',)

    def text_preview(self, obj):
        """Exibe preview do texto do comentário"""
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Comentário'
