from django.db import models
from django.conf import settings


class CipherKey(models.Model):
    """Store user's cipher keys."""
    
    CIPHER_CHOICES = [
        ('caesar', 'Caesar'),
        ('affine', 'Affine'),
        ('hill', 'Hill'),
        ('playfair', 'Playfair'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cipher_keys')
    cipher_type = models.CharField(max_length=20, choices=CIPHER_CHOICES)
    key_name = models.CharField(max_length=100, help_text='Friendly name for this key')
    key_data = models.JSONField(help_text='JSON object containing key parameters')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'cipher_keys'
        ordering = ['-created_at']
        unique_together = ['user', 'key_name']
    
    def __str__(self):
        return f"{self.user.username} - {self.cipher_type} - {self.key_name}"


class EncryptionHistory(models.Model):
    """Log encryption/decryption operations."""
    
    OPERATION_CHOICES = [
        ('encrypt', 'Encrypt'),
        ('decrypt', 'Decrypt'),
    ]
    
    MODE_CHOICES = [
        ('preshared', 'Pre-shared Key'),
        ('embedded', 'Key Embedded in Message'),
        ('sent', 'Key Sent Separately'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='encryption_history')
    cipher_type = models.CharField(max_length=20)
    operation = models.CharField(max_length=10, choices=OPERATION_CHOICES)
    mode = models.CharField(max_length=20, choices=MODE_CHOICES)
    input_text = models.TextField()
    output_text = models.TextField()
    key_used = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'encryption_history'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user.username} - {self.cipher_type} - {self.operation} - {self.timestamp}"
