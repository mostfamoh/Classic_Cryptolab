from rest_framework import serializers
from .models import Exercise, Submission, ActivityLog
from users.serializers import UserSerializer


class ExerciseSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(source='instructor.username', read_only=True)
    submission_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Exercise
        fields = (
            'id', 'instructor', 'instructor_name', 'title', 'description',
            'cipher_type', 'difficulty', 'ciphertext', 'hints', 'points',
            'is_active', 'due_date', 'created_at', 'updated_at', 'submission_count'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'instructor')
        extra_kwargs = {'correct_answer': {'write_only': True}}
    
    def get_submission_count(self, obj):
        return obj.submissions.count()
    
    def create(self, validated_data):
        validated_data['instructor'] = self.context['request'].user
        return super().create(validated_data)


class ExerciseDetailSerializer(ExerciseSerializer):
    """Include correct answer for instructors only."""
    correct_answer = serializers.CharField()
    
    class Meta(ExerciseSerializer.Meta):
        fields = ExerciseSerializer.Meta.fields + ('correct_answer',)


class SubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.username', read_only=True)
    exercise_title = serializers.CharField(source='exercise.title', read_only=True)
    
    class Meta:
        model = Submission
        fields = (
            'id', 'exercise', 'exercise_title', 'student', 'student_name',
            'answer', 'status', 'score', 'feedback', 'submitted_at', 'graded_at'
        )
        read_only_fields = ('id', 'student', 'status', 'score', 'submitted_at', 'graded_at')
    
    def create(self, validated_data):
        validated_data['student'] = self.context['request'].user
        submission = super().create(validated_data)
        # Auto-grade the submission
        submission.auto_grade()
        return submission


class ActivityLogSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = ActivityLog
        fields = ('id', 'user', 'user_name', 'activity_type', 'details', 'timestamp', 'ip_address')
        read_only_fields = ('id', 'timestamp')


class StudentStatsSerializer(serializers.Serializer):
    """Statistics for student dashboard."""
    total_exercises = serializers.IntegerField()
    completed_exercises = serializers.IntegerField()
    total_score = serializers.IntegerField()
    average_score = serializers.FloatField()
    recent_activities = ActivityLogSerializer(many=True)
