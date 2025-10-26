from django.urls import path
from .views import (
    ConversationListCreateView,
    ConversationDetailView,
    MessageListView,
    SendMessageView,
    MITMAttackView,
    InterceptedMessageListView,
    ToggleProtectionView
)

urlpatterns = [
    path('conversations/', ConversationListCreateView.as_view(), name='conversation-list-create'),
    path('conversations/<int:pk>/', ConversationDetailView.as_view(), name='conversation-detail'),
    path('conversations/<int:conversation_id>/messages/', MessageListView.as_view(), name='message-list'),
    path('conversations/<int:conversation_id>/toggle-protection/', ToggleProtectionView.as_view(), name='toggle-protection'),
    path('messages/send/', SendMessageView.as_view(), name='send-message'),
    path('mitm/attack/', MITMAttackView.as_view(), name='mitm-attack'),
    path('mitm/interceptions/', InterceptedMessageListView.as_view(), name='interceptions-list'),
]
