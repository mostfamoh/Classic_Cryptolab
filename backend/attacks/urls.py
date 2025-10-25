from django.urls import path
from .views import (
    CaesarBruteForceView,
    FrequencyAnalysisView,
    HillKnownPlaintextView,
    AttackRecommendationsView,
    AttackLogListView,
    AttackLogDetailView
)

urlpatterns = [
    path('caesar-brute-force/', CaesarBruteForceView.as_view(), name='caesar_brute_force'),
    path('frequency-analysis/', FrequencyAnalysisView.as_view(), name='frequency_analysis'),
    path('hill-known-plaintext/', HillKnownPlaintextView.as_view(), name='hill_known_plaintext'),
    path('recommendations/', AttackRecommendationsView.as_view(), name='attack_recommendations'),
    path('logs/', AttackLogListView.as_view(), name='attack_logs'),
    path('logs/<int:pk>/', AttackLogDetailView.as_view(), name='attack_log_detail'),
]
