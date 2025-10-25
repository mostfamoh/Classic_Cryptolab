from django.urls import path
from .views import (
    CipherOperationView,
    CipherInfoView,
    AllCiphersInfoView,
    CipherKeyListCreateView,
    CipherKeyDetailView,
    EncryptionHistoryListView,
    EncryptionHistoryDetailView
)

urlpatterns = [
    path('operate/', CipherOperationView.as_view(), name='cipher_operate'),
    path('info/', CipherInfoView.as_view(), name='cipher_info'),
    path('info/all/', AllCiphersInfoView.as_view(), name='all_ciphers_info'),
    path('keys/', CipherKeyListCreateView.as_view(), name='cipher_keys'),
    path('keys/<int:pk>/', CipherKeyDetailView.as_view(), name='cipher_key_detail'),
    path('history/', EncryptionHistoryListView.as_view(), name='encryption_history'),
    path('history/<int:pk>/', EncryptionHistoryDetailView.as_view(), name='encryption_history_detail'),
]
