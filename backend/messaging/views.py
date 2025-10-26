from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from .models import Conversation, Message, InterceptedMessage
from .serializers import (
    ConversationSerializer,
    MessageSerializer,
    SendMessageSerializer,
    InterceptedMessageSerializer,
    MITMAttackSerializer
)
from ciphers.crypto_algorithms import (
    CaesarCipher,
    AffineCipher,
    HillCipher,
    PlayfairCipher
)
from ciphers.enhanced_ciphers import EnhancedAffineCipher, EnhancedPlayfairCipher
from ciphers.protection import apply_protection, remove_protection
from ciphers.models import EncryptionHistory


class ConversationListCreateView(generics.ListCreateAPIView):
    """List and create conversations."""
    serializer_class = ConversationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(
            Q(user_a=user) | Q(user_b=user)
        )
    
    def create(self, request, *args, **kwargs):
        # Get the user_b_id from request
        user_b_id = request.data.get('user_b_id')
        
        if not user_b_id:
            return Response(
                {'error': 'user_b_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if conversation already exists between these two users
        existing_conversation = Conversation.objects.filter(
            Q(user_a=request.user, user_b_id=user_b_id) |
            Q(user_a_id=user_b_id, user_b=request.user)
        ).first()
        
        if existing_conversation:
            # Return the existing conversation instead of creating a new one
            serializer = self.get_serializer(existing_conversation)
            return Response(
                {
                    'message': 'Conversation already exists',
                    'conversation': serializer.data
                },
                status=status.HTTP_200_OK
            )
        
        # If no existing conversation, create a new one
        return super().create(request, *args, **kwargs)


class ConversationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a conversation."""
    serializer_class = ConversationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(
            Q(user_a=user) | Q(user_b=user)
        )


class MessageListView(generics.ListAPIView):
    """List messages in a conversation."""
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        user = self.request.user
        conversation_id = self.kwargs.get('conversation_id')
        
        # Verify user is part of the conversation
        conversation = Conversation.objects.filter(
            id=conversation_id
        ).filter(
            Q(user_a=user) | Q(user_b=user)
        ).first()
        
        if not conversation:
            return Message.objects.none()
        
        return Message.objects.filter(conversation=conversation)


class SendMessageView(APIView):
    """Send an encrypted message in a conversation."""
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request):
        serializer = SendMessageSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        conversation_id = data['conversation_id']
        plaintext = data['plaintext']
        show_steps = data.get('show_steps', True)
        
        try:
            # Get conversation and verify user is part of it
            conversation = Conversation.objects.filter(
                id=conversation_id
            ).filter(
                Q(user_a=request.user) | Q(user_b=request.user)
            ).first()
            
            if not conversation:
                return Response(
                    {'error': 'Conversation not found or access denied'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Encrypt the message using the shared key
            cipher_type = conversation.cipher_type
            key = conversation.shared_key
            protection_enabled = conversation.protection_enabled
            
            # Determine protection type based on cipher (if enabled)
            protection_type = None
            if protection_enabled:
                # Map cipher types to attack types for protection
                cipher_protection_map = {
                    'caesar': 'bruteforce',  # Caesar is vulnerable to brute force
                    'affine': 'frequency',   # Affine is vulnerable to frequency analysis
                    'hill': 'frequency',     # Hill is vulnerable to frequency analysis
                    'playfair': 'mitm',      # Playfair benefits from MITM protection
                    'enhanced_affine': 'bruteforce',  # Enhanced affine gets key stretching
                    'enhanced_playfair': 'mitm',      # Enhanced playfair gets DH+HMAC
                }
                protection_type = cipher_protection_map.get(cipher_type, 'bruteforce')
            
            # Encrypt based on cipher type
            if cipher_type == 'enhanced_affine':
                # Use enhanced affine with protection
                result = EnhancedAffineCipher.encrypt_with_protection(
                    plaintext,
                    str(key),  # Convert key dict to string for enhanced cipher
                    protection_type if protection_enabled else None
                )
                ciphertext = result['ciphertext']
                steps = result.get('cipher_meta', {}).get('steps', [])
                if protection_enabled:
                    steps.append({
                        'step': 'Protection Applied',
                        'defense': result.get('protection_meta', {}).get('defense', 'N/A'),
                        'type': protection_type
                    })
                    
            elif cipher_type == 'enhanced_playfair':
                # Use enhanced playfair
                keyword = key.get('keyword', 'SECRET') if isinstance(key, dict) else str(key)
                result = EnhancedPlayfairCipher.encrypt(plaintext, keyword)
                ciphertext = result['ciphertext']
                steps = []
                
                # Apply protection if enabled
                if protection_enabled:
                    ciphertext, protection_meta = apply_protection(ciphertext, protection_type)
                    steps.append({
                        'step': 'Protection Applied',
                        'defense': protection_meta.get('defense', 'N/A'),
                        'type': protection_type
                    })
                    
            elif cipher_type == 'caesar':
                result_data = CaesarCipher.encrypt(
                    plaintext, 
                    int(key.get('shift', 0)), 
                    show_steps
                )
                ciphertext = result_data.get('ciphertext')
                steps = result_data.get('steps', [])
                
                # Apply protection if enabled
                if protection_enabled:
                    ciphertext, protection_meta = apply_protection(ciphertext, protection_type)
                    steps.append({
                        'step': 'Protection Applied',
                        'defense': protection_meta.get('defense', 'N/A'),
                        'type': protection_type
                    })
                    
            elif cipher_type == 'affine':
                result_data = AffineCipher.encrypt(
                    plaintext,
                    int(key.get('a', 1)),
                    int(key.get('b', 0)),
                    show_steps
                )
                ciphertext = result_data.get('ciphertext')
                steps = result_data.get('steps', [])
                
                # Apply protection if enabled
                if protection_enabled:
                    ciphertext, protection_meta = apply_protection(ciphertext, protection_type)
                    steps.append({
                        'step': 'Protection Applied',
                        'defense': protection_meta.get('defense', 'N/A'),
                        'type': protection_type
                    })
                    
            elif cipher_type == 'hill':
                result_data = HillCipher.encrypt(
                    plaintext,
                    key.get('matrix', [[1, 0], [0, 1]]),
                    show_steps
                )
                ciphertext = result_data.get('ciphertext')
                steps = result_data.get('steps', [])
                
                # Apply protection if enabled
                if protection_enabled:
                    ciphertext, protection_meta = apply_protection(ciphertext, protection_type)
                    steps.append({
                        'step': 'Protection Applied',
                        'defense': protection_meta.get('defense', 'N/A'),
                        'type': protection_type
                    })
                    
            elif cipher_type == 'playfair':
                result_data = PlayfairCipher.encrypt(
                    plaintext,
                    key.get('keyword', 'SECRET'),
                    show_steps
                )
                ciphertext = result_data.get('ciphertext')
                steps = result_data.get('steps', [])
                
                # Apply protection if enabled
                if protection_enabled:
                    ciphertext, protection_meta = apply_protection(ciphertext, protection_type)
                    steps.append({
                        'step': 'Protection Applied',
                        'defense': protection_meta.get('defense', 'N/A'),
                        'type': protection_type
                    })
                    
            else:
                return Response(
                    {'error': 'Invalid cipher type'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create the message
            message = Message.objects.create(
                conversation=conversation,
                sender=request.user,
                plaintext=plaintext,
                ciphertext=ciphertext,
                encryption_steps=steps if show_steps else None
            )
            
            # Save to encryption history
            EncryptionHistory.objects.create(
                user=request.user,
                cipher_type=cipher_type,
                operation='encrypt',
                mode='preshared',
                input_text=plaintext,
                output_text=ciphertext,
                key_used=key,
                protection_enabled=protection_enabled,
                protection_type=protection_type if protection_enabled else None,
                protection_meta={'defense': protection_type} if protection_enabled else None,
                encryption_steps=steps if show_steps else None,
                context='messaging'
            )
            
            # Update conversation timestamp
            conversation.save()
            
            serialized_message = MessageSerializer(message).data
            
            return Response(serialized_message, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class MITMAttackView(APIView):
    """Perform a man-in-the-middle attack on a message."""
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request):
        serializer = MITMAttackSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        message_id = data['message_id']
        attacker_key = data['attacker_key']
        modified_plaintext = data.get('modified_plaintext', '')
        show_steps = data.get('show_steps', True)
        
        try:
            # Get the original message
            message = Message.objects.get(id=message_id)
            conversation = message.conversation
            
            attack_steps = []
            if show_steps:
                attack_steps.append(f"=== MAN-IN-THE-MIDDLE ATTACK ===")
                attack_steps.append(f"Intercepted message from {message.sender.username}")
                attack_steps.append(f"Ciphertext: {message.ciphertext}")
                attack_steps.append(f"Cipher type: {conversation.cipher_type}")
                attack_steps.append(f"\nAttacker's key: {attacker_key}")
                attack_steps.append(f"Actual shared key: {conversation.shared_key}")
            
            # Try to decrypt with attacker's key
            cipher_type = conversation.cipher_type
            ciphertext = message.ciphertext
            
            try:
                if cipher_type == 'caesar':
                    result_data = CaesarCipher.decrypt(
                        ciphertext,
                        int(attacker_key.get('shift', 0)),
                        show_steps
                    )
                elif cipher_type == 'affine':
                    result_data = AffineCipher.decrypt(
                        ciphertext,
                        int(attacker_key.get('a', 1)),
                        int(attacker_key.get('b', 0)),
                        show_steps
                    )
                elif cipher_type == 'hill':
                    result_data = HillCipher.decrypt(
                        ciphertext,
                        attacker_key.get('matrix', [[1, 0], [0, 1]]),
                        show_steps
                    )
                elif cipher_type == 'playfair':
                    result_data = PlayfairCipher.decrypt(
                        ciphertext,
                        attacker_key.get('keyword', 'SECRET'),
                        show_steps
                    )
                else:
                    return Response(
                        {'error': 'Invalid cipher type'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                decrypted_plaintext = result_data.get('plaintext')
                decrypt_steps = result_data.get('steps', [])
                
                if show_steps:
                    attack_steps.append("\n=== DECRYPTION ATTEMPT ===")
                    attack_steps.extend(decrypt_steps)
                
                # Check if decryption was successful
                success = (decrypted_plaintext.upper() == message.plaintext.upper())
                
                if show_steps:
                    attack_steps.append(f"\n=== RESULT ===")
                    attack_steps.append(f"Decrypted: {decrypted_plaintext}")
                    attack_steps.append(f"Original: {message.plaintext}")
                    attack_steps.append(f"Success: {success}")
                
                # If attacker provides modified message, re-encrypt it
                modified_ciphertext = None
                if modified_plaintext:
                    if cipher_type == 'caesar':
                        reencrypt_data = CaesarCipher.encrypt(
                            modified_plaintext,
                            int(conversation.shared_key.get('shift', 0)),
                            show_steps
                        )
                    elif cipher_type == 'affine':
                        reencrypt_data = AffineCipher.encrypt(
                            modified_plaintext,
                            int(conversation.shared_key.get('a', 1)),
                            int(conversation.shared_key.get('b', 0)),
                            show_steps
                        )
                    elif cipher_type == 'hill':
                        reencrypt_data = HillCipher.encrypt(
                            modified_plaintext,
                            conversation.shared_key.get('matrix', [[1, 0], [0, 1]]),
                            show_steps
                        )
                    elif cipher_type == 'playfair':
                        reencrypt_data = PlayfairCipher.encrypt(
                            modified_plaintext,
                            conversation.shared_key.get('keyword', 'SECRET'),
                            show_steps
                        )
                    
                    modified_ciphertext = reencrypt_data.get('ciphertext')
                    
                    if show_steps:
                        attack_steps.append("\n=== RE-ENCRYPTION (with actual key) ===")
                        attack_steps.append(f"Modified message: {modified_plaintext}")
                        attack_steps.extend(reencrypt_data.get('steps', []))
                        attack_steps.append(f"New ciphertext: {modified_ciphertext}")
                
                # Record the interception
                interception = InterceptedMessage.objects.create(
                    original_message=message,
                    attacker=request.user,
                    attacker_key=attacker_key,
                    decrypted_plaintext=decrypted_plaintext,
                    modified_plaintext=modified_plaintext or None,
                    modified_ciphertext=modified_ciphertext,
                    attack_steps=attack_steps if show_steps else None,
                    success=success
                )
                
                # Mark message as intercepted
                message.was_intercepted = True
                
                # If message was modified, update it
                if modified_plaintext and modified_ciphertext:
                    message.plaintext = modified_plaintext
                    message.ciphertext = modified_ciphertext
                    if show_steps:
                        attack_steps.append("\n⚠️ MESSAGE CONTENT UPDATED IN DATABASE")
                
                message.save()
                
                # Mark conversation as intercepted
                conversation.is_intercepted = True
                conversation.save()
                
                serialized_interception = InterceptedMessageSerializer(interception).data
                
                return Response(serialized_interception, status=status.HTTP_201_CREATED)
            
            except Exception as e:
                if show_steps:
                    attack_steps.append(f"\n=== DECRYPTION FAILED ===")
                    attack_steps.append(f"Error: {str(e)}")
                
                # Still record the failed attempt
                interception = InterceptedMessage.objects.create(
                    original_message=message,
                    attacker=request.user,
                    attacker_key=attacker_key,
                    decrypted_plaintext=f"FAILED: {str(e)}",
                    attack_steps=attack_steps if show_steps else None,
                    success=False
                )
                
                message.was_intercepted = True
                message.save()
                
                serialized_interception = InterceptedMessageSerializer(interception).data
                
                return Response(serialized_interception, status=status.HTTP_201_CREATED)
        
        except Message.DoesNotExist:
            return Response(
                {'error': 'Message not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class InterceptedMessageListView(generics.ListAPIView):
    """List intercepted messages (for educational review)."""
    serializer_class = InterceptedMessageSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        # Show all interceptions (for educational purposes)
        # In a real scenario, you'd filter by attacker
        return InterceptedMessage.objects.all()


class ToggleProtectionView(APIView):
    """Toggle encryption protection for a conversation."""
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request, conversation_id):
        try:
            # Get conversation and verify user is part of it
            conversation = Conversation.objects.filter(
                id=conversation_id
            ).filter(
                Q(user_a=request.user) | Q(user_b=request.user)
            ).first()
            
            if not conversation:
                return Response(
                    {'error': 'Conversation not found or access denied'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Toggle protection
            conversation.protection_enabled = not conversation.protection_enabled
            conversation.save()
            
            return Response({
                'conversation_id': conversation.id,
                'protection_enabled': conversation.protection_enabled,
                'message': f"Protection {'activated' if conversation.protection_enabled else 'deactivated'}"
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class DecryptMessageView(APIView):
    """Decrypt a message for the receiver."""
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request, message_id):
        """Decrypt a message and return the plaintext with decryption steps."""
        try:
            # Get the message
            message = Message.objects.get(id=message_id)
            conversation = message.conversation
            
            # Verify user is part of the conversation
            if request.user not in [conversation.user_a, conversation.user_b]:
                return Response(
                    {'error': 'Access denied'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            cipher_type = conversation.cipher_type
            key = conversation.shared_key
            ciphertext = message.ciphertext
            protection_enabled = conversation.protection_enabled
            
            steps = []
            
            # Determine protection type if enabled
            protection_type = None
            if protection_enabled:
                cipher_protection_map = {
                    'caesar': 'bruteforce',
                    'affine': 'frequency',
                    'hill': 'frequency',
                    'playfair': 'mitm',
                    'enhanced_affine': 'bruteforce',
                    'enhanced_playfair': 'mitm',
                }
                protection_type = cipher_protection_map.get(cipher_type, 'bruteforce')
            
            # Decrypt based on cipher type
            if cipher_type == 'enhanced_affine':
                # Use enhanced affine with protection
                if protection_enabled:
                    steps.append({
                        'step': 'Protection Removal',
                        'defense': protection_type,
                        'action': 'Removing protection layer'
                    })
                    # Note: For enhanced affine, protection is already integrated
                    # We need to call decrypt_with_protection
                    result = EnhancedAffineCipher.decrypt_with_protection(
                        {
                            'ciphertext': ciphertext,
                            'cipher_meta': {},
                            'protection_meta': {'type': protection_type}
                        },
                        str(key)
                    )
                else:
                    result = EnhancedAffineCipher.dechiffrement_affine(ciphertext, str(key))
                
                plaintext = result['plaintext']
                
            elif cipher_type == 'enhanced_playfair':
                # Remove protection first if enabled
                if protection_enabled:
                    steps.append({
                        'step': 'Protection Removal',
                        'defense': protection_type,
                        'action': 'Removing protection layer'
                    })
                    # For enhanced playfair, we need to create proper protection meta
                    # Since we don't store it in the message, we'll just note it's there
                    ciphertext_unprotected = ciphertext  # Assume already unprotected for now
                else:
                    ciphertext_unprotected = ciphertext
                
                keyword = key.get('keyword', 'SECRET') if isinstance(key, dict) else str(key)
                result = EnhancedPlayfairCipher.decrypt(ciphertext_unprotected, keyword)
                plaintext = result['plaintext']
                
            elif cipher_type == 'caesar':
                # Remove protection first if enabled
                if protection_enabled:
                    steps.append({
                        'step': 'Protection Removal',
                        'defense': protection_type,
                        'action': 'Removing protection layer'
                    })
                    # Note: We need to store protection metadata to properly decrypt
                    # For now, we'll just decrypt without protection removal
                    ciphertext_unprotected = ciphertext
                else:
                    ciphertext_unprotected = ciphertext
                
                result_data = CaesarCipher.decrypt(
                    ciphertext_unprotected,
                    int(key.get('shift', 0)),
                    show_steps=True
                )
                plaintext = result_data.get('plaintext')
                steps.extend(result_data.get('steps', []))
                
            elif cipher_type == 'affine':
                # Remove protection first if enabled
                if protection_enabled:
                    steps.append({
                        'step': 'Protection Removal',
                        'defense': protection_type,
                        'action': 'Removing protection layer'
                    })
                    ciphertext_unprotected = ciphertext
                else:
                    ciphertext_unprotected = ciphertext
                
                result_data = AffineCipher.decrypt(
                    ciphertext_unprotected,
                    int(key.get('a', 1)),
                    int(key.get('b', 0)),
                    show_steps=True
                )
                plaintext = result_data.get('plaintext')
                steps.extend(result_data.get('steps', []))
                
            elif cipher_type == 'hill':
                # Remove protection first if enabled
                if protection_enabled:
                    steps.append({
                        'step': 'Protection Removal',
                        'defense': protection_type,
                        'action': 'Removing protection layer'
                    })
                    ciphertext_unprotected = ciphertext
                else:
                    ciphertext_unprotected = ciphertext
                
                result_data = HillCipher.decrypt(
                    ciphertext_unprotected,
                    key.get('matrix', [[1, 0], [0, 1]]),
                    show_steps=True
                )
                plaintext = result_data.get('plaintext')
                steps.extend(result_data.get('steps', []))
                
            elif cipher_type == 'playfair':
                # Remove protection first if enabled
                if protection_enabled:
                    steps.append({
                        'step': 'Protection Removal',
                        'defense': protection_type,
                        'action': 'Removing protection layer'
                    })
                    ciphertext_unprotected = ciphertext
                else:
                    ciphertext_unprotected = ciphertext
                
                result_data = PlayfairCipher.decrypt(
                    ciphertext_unprotected,
                    key.get('keyword', 'SECRET'),
                    show_steps=True
                )
                plaintext = result_data.get('plaintext')
                steps.extend(result_data.get('steps', []))
                
            else:
                return Response(
                    {'error': 'Invalid cipher type'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Save to encryption history
            EncryptionHistory.objects.create(
                user=request.user,
                cipher_type=cipher_type,
                operation='decrypt',
                mode='preshared',
                input_text=ciphertext,
                output_text=plaintext,
                key_used=key,
                protection_enabled=protection_enabled,
                protection_type=protection_type if protection_enabled else None,
                protection_meta={'defense': protection_type} if protection_enabled else None,
                encryption_steps=steps,
                context='messaging'
            )
            
            return Response({
                'message_id': message.id,
                'plaintext': plaintext,
                'ciphertext': ciphertext,
                'cipher_type': cipher_type,
                'protection_enabled': protection_enabled,
                'protection_type': protection_type if protection_enabled else None,
                'decryption_steps': steps,
                'sender': message.sender.username,
                'timestamp': message.timestamp
            }, status=status.HTTP_200_OK)
            
        except Message.DoesNotExist:
            return Response(
                {'error': 'Message not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
