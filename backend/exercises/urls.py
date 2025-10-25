from django.urls import path
from .views import (
    ExerciseListCreateView,
    ExerciseDetailView,
    SubmissionListCreateView,
    SubmissionDetailView,
    StudentStatsView,
    InstructorDashboardView,
    ActivityLogListView,
    LogActivityView
)

urlpatterns = [
    path('', ExerciseListCreateView.as_view(), name='exercises'),
    path('<int:pk>/', ExerciseDetailView.as_view(), name='exercise_detail'),
    path('submissions/', SubmissionListCreateView.as_view(), name='submissions'),
    path('submissions/<int:pk>/', SubmissionDetailView.as_view(), name='submission_detail'),
    path('student-stats/', StudentStatsView.as_view(), name='student_stats'),
    path('instructor-dashboard/', InstructorDashboardView.as_view(), name='instructor_dashboard'),
    path('activity-logs/', ActivityLogListView.as_view(), name='activity_logs'),
    path('log-activity/', LogActivityView.as_view(), name='log_activity'),
]
