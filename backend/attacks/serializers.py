from rest_framework import serializers
from .models import AttackLog


class AttackLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttackLog
        fields = ('id', 'cipher_type', 'attack_type', 'target_text', 'results', 'success', 'timestamp')
        read_only_fields = ('id', 'timestamp')


class CaesarBruteForceSerializer(serializers.Serializer):
    ciphertext = serializers.CharField()
    log_attack = serializers.BooleanField(default=True)


class FrequencyAnalysisSerializer(serializers.Serializer):
    text = serializers.CharField()
    log_attack = serializers.BooleanField(default=True)


class HillKnownPlaintextSerializer(serializers.Serializer):
    plaintext = serializers.CharField(min_length=4)
    ciphertext = serializers.CharField(min_length=4)
    log_attack = serializers.BooleanField(default=True)


class AttackRecommendationsSerializer(serializers.Serializer):
    cipher_type = serializers.ChoiceField(choices=['caesar', 'affine', 'hill', 'playfair'])
