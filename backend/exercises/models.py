from django.db import models
from django.conf import settings


class Exercise(models.Model):
    """Exercises created by instructors."""
    
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_exercises',
        limit_choices_to={'role': 'instructor'}
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    cipher_type = models.CharField(max_length=20)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    ciphertext = models.TextField(help_text='The encrypted text students need to decrypt')
    correct_answer = models.TextField(help_text='The expected plaintext answer')
    hints = models.JSONField(default=list, blank=True)
    points = models.IntegerField(default=10)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'exercises'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.cipher_type})"


class Submission(models.Model):
    """Student submissions for exercises."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('correct', 'Correct'),
        ('incorrect', 'Incorrect'),
        ('partially_correct', 'Partially Correct'),
    ]
    
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='exercise_submissions',
        limit_choices_to={'role': 'student'}
    )
    answer = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    score = models.IntegerField(default=0)
    feedback = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    graded_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'submissions'
        ordering = ['-submitted_at']
        unique_together = ['exercise', 'student']
    
    def __str__(self):
        return f"{self.student.username} - {self.exercise.title}"
    
    def auto_grade(self):
        """Automatically grade the submission."""
        from django.utils import timezone
        
        # Simple exact match for now
        if self.answer.strip().upper() == self.exercise.correct_answer.strip().upper():
            self.status = 'correct'
            self.score = self.exercise.points
        else:
            # Check partial match (similarity)
            answer_set = set(self.answer.strip().upper().split())
            correct_set = set(self.exercise.correct_answer.strip().upper().split())
            
            if answer_set & correct_set:  # If there's any overlap
                similarity = len(answer_set & correct_set) / len(correct_set)
                if similarity > 0.7:
                    self.status = 'partially_correct'
                    self.score = int(self.exercise.points * similarity)
                else:
                    self.status = 'incorrect'
                    self.score = 0
            else:
                self.status = 'incorrect'
                self.score = 0
        
        self.graded_at = timezone.now()
        self.save()


class ActivityLog(models.Model):
    """Log all student activities for instructor monitoring."""
    
    ACTIVITY_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('encrypt', 'Encryption'),
        ('decrypt', 'Decryption'),
        ('attack', 'Attack Simulation'),
        ('exercise_view', 'View Exercise'),
        ('exercise_submit', 'Submit Exercise'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activity_logs')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_CHOICES)
    details = models.JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        db_table = 'activity_logs'
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user.username} - {self.activity_type} - {self.timestamp}"
