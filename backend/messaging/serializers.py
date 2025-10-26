from rest_framework import serializers
from .models import Conversation, Message, InterceptedMessage
from django.contrib.auth import get_user_model

User = get_user_model()


class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class ConversationSerializer(serializers.ModelSerializer):
    user_a = UserBasicSerializer(read_only=True)
    user_b = UserBasicSerializer(read_only=True)
    user_a_id = serializers.IntegerField(write_only=True, required=False)
    user_b_id = serializers.IntegerField(write_only=True)
    message_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ('id', 'user_a', 'user_b', 'user_a_id', 'user_b_id', 'cipher_type', 
                  'shared_key', 'is_intercepted', 'protection_enabled', 'created_at', 'updated_at', 'message_count')
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def get_message_count(self, obj):
        return obj.messages.count()
    
    def create(self, validated_data):
        user_a_id = validated_data.pop('user_a_id', None)
        user_b_id = validated_data.pop('user_b_id')
        
        # Set user_a to current user if not provided
        if not user_a_id:
            user_a = self.context['request'].user
        else:
            user_a = User.objects.get(id=user_a_id)
        
        user_b = User.objects.get(id=user_b_id)
        
        validated_data['user_a'] = user_a
        validated_data['user_b'] = user_b
        
        return super().create(validated_data)


class MessageSerializer(serializers.ModelSerializer):
    sender = UserBasicSerializer(read_only=True)
    sender_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Message
        fields = ('id', 'conversation', 'sender', 'sender_id', 'plaintext', 'ciphertext',
                  'encryption_steps', 'timestamp', 'is_read', 'was_intercepted')
        read_only_fields = ('id', 'timestamp', 'was_intercepted')
    
    def create(self, validated_data):
        sender_id = validated_data.pop('sender_id', None)
        
        if not sender_id:
            validated_data['sender'] = self.context['request'].user
        else:
            validated_data['sender'] = User.objects.get(id=sender_id)
        
        return super().create(validated_data)


class SendMessageSerializer(serializers.Serializer):
    """Serializer for sending an encrypted message."""
    conversation_id = serializers.IntegerField()
    plaintext = serializers.CharField()
    show_steps = serializers.BooleanField(default=True)


class InterceptedMessageSerializer(serializers.ModelSerializer):
    attacker = UserBasicSerializer(read_only=True)
    original_message = MessageSerializer(read_only=True)
    
    class Meta:
        model = InterceptedMessage
        fields = ('id', 'original_message', 'attacker', 'attacker_key', 
                  'decrypted_plaintext', 'modified_plaintext', 'modified_ciphertext',
                  'attack_steps', 'timestamp', 'success')
        read_only_fields = ('id', 'timestamp')


class MITMAttackSerializer(serializers.Serializer):
    """Serializer for performing a man-in-the-middle attack."""
    message_id = serializers.IntegerField()
    attacker_key = serializers.JSONField()
    modified_plaintext = serializers.CharField(required=False, allow_blank=True)
    show_steps = serializers.BooleanField(default=True)
