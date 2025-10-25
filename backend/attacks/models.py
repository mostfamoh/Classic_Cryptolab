from django.db import models
from django.conf import settings


class AttackLog(models.Model):
    """Log cryptanalysis attacks performed by users."""
    
    ATTACK_CHOICES = [
        ('brute_force', 'Brute Force'),
        ('frequency_analysis', 'Frequency Analysis'),
        ('known_plaintext', 'Known Plaintext'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attack_logs')
    cipher_type = models.CharField(max_length=20)
    attack_type = models.CharField(max_length=30, choices=ATTACK_CHOICES)
    target_text = models.TextField()
    results = models.JSONField()
    success = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'attack_logs'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user.username} - {self.attack_type} on {self.cipher_type} - {self.timestamp}"
