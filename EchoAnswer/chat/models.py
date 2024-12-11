from django.db import models

class Chat(models.Model):
    user_input = models.TextField()
    bot_response = models.TextField()
    context = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat {self.id} - {self.created_at}"
