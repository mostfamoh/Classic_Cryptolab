from rest_framework import serializers
from .models import CipherKey, EncryptionHistory


class CipherKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = CipherKey
        fields = ('id', 'cipher_type', 'key_name', 'key_data', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class EncryptionHistorySerializer(serializers.ModelSerializer):
    protection_type_display = serializers.SerializerMethodField()
    
    class Meta:
        model = EncryptionHistory
        fields = (
            'id', 'cipher_type', 'operation', 'mode', 
            'input_text', 'output_text', 'key_used', 
            'protection_enabled', 'protection_type', 'protection_type_display',
            'protection_meta', 'encryption_steps', 'context',
            'timestamp'
        )
        read_only_fields = ('id', 'timestamp')
    
    def get_protection_type_display(self, obj):
        """Get human-readable protection type."""
        if not obj.protection_enabled:
            return 'No Protection'
        
        protection_map = {
            'bruteforce': '🛡️ Argon2 Key Stretching',
            'frequency': '🔊 Frequency Noise Injection',
            'mitm': '🤝 Diffie-Hellman + HMAC',
        }
        return protection_map.get(obj.protection_type, obj.protection_type)
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class CipherOperationSerializer(serializers.Serializer):
    """Serializer for cipher encrypt/decrypt operations."""
    cipher_type = serializers.ChoiceField(choices=['caesar', 'affine', 'hill', 'playfair'])
    operation = serializers.ChoiceField(choices=['encrypt', 'decrypt'])
    text = serializers.CharField()
    key = serializers.JSONField()
    mode = serializers.ChoiceField(
        choices=['preshared', 'embedded', 'sent'],
        default='preshared'
    )
    log_operation = serializers.BooleanField(default=True)
    show_steps = serializers.BooleanField(default=False)


class CipherInfoSerializer(serializers.Serializer):
    """Serializer for cipher information."""
    cipher_type = serializers.ChoiceField(choices=['caesar', 'affine', 'hill', 'playfair'])
