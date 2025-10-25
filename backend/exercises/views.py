from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Sum, Avg
from .models import Exercise, Submission, ActivityLog
from .serializers import (
    ExerciseSerializer,
    ExerciseDetailSerializer,
    SubmissionSerializer,
    ActivityLogSerializer,
    StudentStatsSerializer
)


class IsInstructor(permissions.BasePermission):
    """Custom permission to only allow instructors."""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'instructor'


class ExerciseListCreateView(generics.ListCreateAPIView):
    """List exercises (all users) and create exercises (instructors only)."""
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_serializer_class(self):
        if self.request.method == 'POST' or (self.request.user and self.request.user.is_instructor()):
            return ExerciseDetailSerializer
        return ExerciseSerializer
    
    def get_queryset(self):
        queryset = Exercise.objects.filter(is_active=True)
        
        # Students see all active exercises
        # Instructors see their own exercises
        if self.request.user.is_instructor():
            queryset = Exercise.objects.filter(instructor=self.request.user)
        
        # Filter by cipher type
        cipher_type = self.request.query_params.get('cipher_type', None)
        if cipher_type:
            queryset = queryset.filter(cipher_type=cipher_type)
        
        # Filter by difficulty
        difficulty = self.request.query_params.get('difficulty', None)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        return queryset
    
    def perform_create(self, serializer):
        # Only instructors can create exercises
        if not self.request.user.is_instructor():
            raise permissions.PermissionDenied("Only instructors can create exercises")
        serializer.save()


class ExerciseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete an exercise."""
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_serializer_class(self):
        if self.request.user and self.request.user.is_instructor():
            return ExerciseDetailSerializer
        return ExerciseSerializer
    
    def get_queryset(self):
        if self.request.user.is_instructor():
            return Exercise.objects.filter(instructor=self.request.user)
        return Exercise.objects.filter(is_active=True)
    
    def perform_update(self, serializer):
        # Only instructors can update their own exercises
        if not self.request.user.is_instructor():
            raise permissions.PermissionDenied("Only instructors can update exercises")
        serializer.save()
    
    def perform_destroy(self, instance):
        # Only instructors can delete their own exercises
        if not self.request.user.is_instructor():
            raise permissions.PermissionDenied("Only instructors can delete exercises")
        instance.delete()


class SubmissionListCreateView(generics.ListCreateAPIView):
    """List and create submissions."""
    serializer_class = SubmissionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        if self.request.user.is_instructor():
            # Instructors see all submissions for their exercises
            return Submission.objects.filter(exercise__instructor=self.request.user)
        else:
            # Students see only their own submissions
            return Submission.objects.filter(student=self.request.user)
    
    def perform_create(self, serializer):
        # Only students can submit
        if self.request.user.is_instructor():
            raise permissions.PermissionDenied("Instructors cannot submit exercises")
        
        # Log the activity
        ActivityLog.objects.create(
            user=self.request.user,
            activity_type='exercise_submit',
            details={'exercise_id': serializer.validated_data['exercise'].id}
        )
        
        serializer.save()


class SubmissionDetailView(generics.RetrieveUpdateAPIView):
    """Retrieve and update a submission (for instructor grading)."""
    serializer_class = SubmissionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        if self.request.user.is_instructor():
            return Submission.objects.filter(exercise__instructor=self.request.user)
        return Submission.objects.filter(student=self.request.user)
    
    def perform_update(self, serializer):
        # Only instructors can update submissions (for manual grading)
        if not self.request.user.is_instructor():
            raise permissions.PermissionDenied("Only instructors can grade submissions")
        serializer.save()


class StudentStatsView(APIView):
    """Get statistics for student dashboard."""
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request):
        if request.user.is_instructor():
            return Response({"error": "This endpoint is for students only"}, status=status.HTTP_403_FORBIDDEN)
        
        # Get student's submissions
        submissions = Submission.objects.filter(student=request.user)
        
        # Calculate stats
        stats = {
            'total_exercises': Exercise.objects.filter(is_active=True).count(),
            'completed_exercises': submissions.count(),
            'total_score': submissions.aggregate(Sum('score'))['score__sum'] or 0,
            'average_score': submissions.aggregate(Avg('score'))['score__avg'] or 0,
            'recent_activities': ActivityLogSerializer(
                ActivityLog.objects.filter(user=request.user)[:10],
                many=True
            ).data
        }
        
        return Response(stats, status=status.HTTP_200_OK)


class InstructorDashboardView(APIView):
    """Get statistics for instructor dashboard."""
    permission_classes = (IsInstructor,)
    
    def get(self, request):
        # Get instructor's exercises
        exercises = Exercise.objects.filter(instructor=request.user)
        
        # Get all submissions for instructor's exercises
        submissions = Submission.objects.filter(exercise__instructor=request.user)
        
        # Get unique students who have submitted
        students_count = submissions.values('student').distinct().count()
        
        stats = {
            'total_exercises': exercises.count(),
            'active_exercises': exercises.filter(is_active=True).count(),
            'total_submissions': submissions.count(),
            'active_students': students_count,
            'average_score': submissions.aggregate(Avg('score'))['score__avg'] or 0,
            'recent_submissions': SubmissionSerializer(
                submissions.order_by('-submitted_at')[:10],
                many=True
            ).data,
            'exercises_by_cipher': list(
                exercises.values('cipher_type').annotate(count=Count('id'))
            ),
            'submissions_by_status': list(
                submissions.values('status').annotate(count=Count('id'))
            )
        }
        
        return Response(stats, status=status.HTTP_200_OK)


class ActivityLogListView(generics.ListAPIView):
    """List activity logs."""
    serializer_class = ActivityLogSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        if self.request.user.is_instructor():
            # Instructors see all student activities
            return ActivityLog.objects.filter(user__role='student')
        else:
            # Students see only their own activities
            return ActivityLog.objects.filter(user=self.request.user)


class LogActivityView(APIView):
    """Manually log an activity."""
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request):
        activity_type = request.data.get('activity_type')
        details = request.data.get('details', {})
        
        if not activity_type:
            return Response({"error": "activity_type is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        log = ActivityLog.objects.create(
            user=request.user,
            activity_type=activity_type,
            details=details,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return Response(ActivityLogSerializer(log).data, status=status.HTTP_201_CREATED)
