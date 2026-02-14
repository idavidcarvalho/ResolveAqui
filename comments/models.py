from django.db import models
from django.conf import settings
from tickets.models import Ticket


class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=500, verbose_name='Comentário')
    photo = models.ImageField(upload_to='comments/photos/', null=True, blank=True, verbose_name='Foto')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'

    def __str__(self):
        return f"Comentário de {self.author.firstName} em {self.ticket}"
