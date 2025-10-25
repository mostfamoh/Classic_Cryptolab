from django.db import models
from django.conf import settings


class Conversation(models.Model):
    """A conversation between two users."""
    user_a = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='conversations_as_a'
    )
    user_b = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='conversations_as_b'
    )
    cipher_type = models.CharField(
        max_length=20,
        choices=[
            ('caesar', 'Caesar'),
            ('affine', 'Affine'),
            ('hill', 'Hill'),
            ('playfair', 'Playfair'),
        ]
    )
    shared_key = models.JSONField(
        help_text='Shared encryption key between A and B'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_intercepted = models.BooleanField(
        default=False,
        help_text='Whether this conversation is under MITM attack'
    )
    
    class Meta:
        db_table = 'conversations'
        ordering = ['-updated_at']
        unique_together = ['user_a', 'user_b']
    
    def __str__(self):
        return f"{self.user_a.username} <-> {self.user_b.username} ({self.cipher_type})"
    
    def get_other_user(self, user):
        """Get the other user in this conversation."""
        return self.user_b if user == self.user_a else self.user_a


class Message(models.Model):
    """A message in a conversation."""
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    plaintext = models.TextField(
        help_text='Original plaintext message (for educational purposes)'
    )
    ciphertext = models.TextField(
        help_text='Encrypted message'
    )
    encryption_steps = models.JSONField(
        null=True,
        blank=True,
        help_text='Step-by-step encryption process'
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    was_intercepted = models.BooleanField(
        default=False,
        help_text='Whether this message was intercepted by MITM'
    )
    
    class Meta:
        db_table = 'messages'
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.sender.username} @ {self.timestamp}: {self.plaintext[:30]}..."


class InterceptedMessage(models.Model):
    """Record of a man-in-the-middle attack on a message."""
    original_message = models.OneToOneField(
        Message,
        on_delete=models.CASCADE,
        related_name='interception'
    )
    attacker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='intercepted_messages'
    )
    attacker_key = models.JSONField(
        help_text='Key the attacker thinks is being used'
    )
    decrypted_plaintext = models.TextField(
        help_text='What the attacker decrypted'
    )
    modified_plaintext = models.TextField(
        null=True,
        blank=True,
        help_text='Modified message from attacker'
    )
    modified_ciphertext = models.TextField(
        null=True,
        blank=True,
        help_text='Re-encrypted modified message'
    )
    attack_steps = models.JSONField(
        null=True,
        blank=True,
        help_text='Step-by-step MITM attack process'
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(
        default=False,
        help_text='Whether the attack successfully decrypted the message'
    )
    
    class Meta:
        db_table = 'intercepted_messages'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"MITM by {self.attacker.username} on message {self.original_message.id}"

