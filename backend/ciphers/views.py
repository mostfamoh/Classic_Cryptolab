from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CipherKey, EncryptionHistory
from .serializers import (
    CipherKeySerializer,
    EncryptionHistorySerializer,
    CipherOperationSerializer,
    CipherInfoSerializer
)
from .crypto_algorithms import (
    CaesarCipher,
    AffineCipher,
    HillCipher,
    PlayfairCipher
)


class CipherOperationView(APIView):
    """Handle cipher encryption/decryption operations."""
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request):
        serializer = CipherOperationSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        cipher_type = data['cipher_type']
        operation = data['operation']
        text = data['text']
        key = data['key']
        mode = data.get('mode', 'preshared')
        log_operation = data.get('log_operation', True)
        show_steps = data.get('show_steps', False)
        
        try:
            # Perform encryption/decryption
            if cipher_type == 'caesar':
                cipher = CaesarCipher()
                key_int = int(key.get('shift', 0))
                result_data = cipher.encrypt(text, key_int, show_steps) if operation == 'encrypt' else cipher.decrypt(text, key_int, show_steps)
            
            elif cipher_type == 'affine':
                cipher = AffineCipher()
                key_a = int(key.get('a', 1))
                key_b = int(key.get('b', 0))
                result_data = cipher.encrypt(text, key_a, key_b, show_steps) if operation == 'encrypt' else cipher.decrypt(text, key_a, key_b, show_steps)
            
            elif cipher_type == 'hill':
                cipher = HillCipher()
                # Support both text key and matrix key
                if isinstance(key, str):
                    # Text key provided
                    key_input = key
                elif 'text_key' in key:
                    # Text key in dictionary
                    key_input = key.get('text_key')
                else:
                    # Matrix key provided
                    key_input = key.get('matrix', [[1, 0], [0, 1]])
                
                result_data = cipher.encrypt(text, key_input, show_steps) if operation == 'encrypt' else cipher.decrypt(text, key_input, show_steps)
            
            elif cipher_type == 'playfair':
                cipher = PlayfairCipher()
                key_word = key.get('keyword', 'SECRET')
                result_data = cipher.encrypt(text, key_word, show_steps) if operation == 'encrypt' else cipher.decrypt(text, key_word, show_steps)
            
            else:
                return Response({'error': 'Invalid cipher type'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Extract result text
            result_text = result_data.get('ciphertext') or result_data.get('plaintext')
            steps = result_data.get('steps', []) if show_steps else None
            
            # Log operation if requested
            if log_operation:
                EncryptionHistory.objects.create(
                    user=request.user,
                    cipher_type=cipher_type,
                    operation=operation,
                    mode=mode,
                    input_text=text,
                    output_text=result_text,
                    key_used=key,
                    protection_enabled=False,  # No protection for standalone operations
                    encryption_steps=steps,
                    context='standalone'
                )
            
            response_data = {
                'result': result_text,
                'cipher_type': cipher_type,
                'operation': operation,
                'mode': mode
            }
            
            if show_steps and 'steps' in result_data:
                response_data['steps'] = result_data['steps']
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CipherInfoView(APIView):
    """Get information about a specific cipher."""
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request):
        serializer = CipherInfoSerializer(data=request.query_params)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        cipher_type = serializer.validated_data['cipher_type']
        
        info_map = {
            'caesar': CaesarCipher.get_info(),
            'affine': AffineCipher.get_info(),
            'hill': HillCipher.get_info(),
            'playfair': PlayfairCipher.get_info()
        }
        
        return Response(info_map.get(cipher_type, {}), status=status.HTTP_200_OK)


class AllCiphersInfoView(APIView):
    """Get information about all ciphers."""
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request):
        return Response({
            'caesar': CaesarCipher.get_info(),
            'affine': AffineCipher.get_info(),
            'hill': HillCipher.get_info(),
            'playfair': PlayfairCipher.get_info()
        }, status=status.HTTP_200_OK)


class CipherKeyListCreateView(generics.ListCreateAPIView):
    """List and create cipher keys."""
    serializer_class = CipherKeySerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        return CipherKey.objects.filter(user=self.request.user)


class CipherKeyDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a cipher key."""
    serializer_class = CipherKeySerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        return CipherKey.objects.filter(user=self.request.user)


class EncryptionHistoryListView(generics.ListAPIView):
    """List encryption history for the current user with advanced filtering."""
    serializer_class = EncryptionHistorySerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        queryset = EncryptionHistory.objects.filter(user=self.request.user)
        
        # Filter by cipher type if provided
        cipher_type = self.request.query_params.get('cipher_type', None)
        if cipher_type:
            queryset = queryset.filter(cipher_type=cipher_type)
        
        # Filter by operation if provided
        operation = self.request.query_params.get('operation', None)
        if operation:
            queryset = queryset.filter(operation=operation)
        
        # Filter by protection enabled
        protection_enabled = self.request.query_params.get('protection_enabled', None)
        if protection_enabled is not None:
            queryset = queryset.filter(protection_enabled=protection_enabled.lower() == 'true')
        
        # Filter by protection type
        protection_type = self.request.query_params.get('protection_type', None)
        if protection_type:
            queryset = queryset.filter(protection_type=protection_type)
        
        # Filter by context
        context = self.request.query_params.get('context', None)
        if context:
            queryset = queryset.filter(context=context)
        
        # Limit results
        limit = self.request.query_params.get('limit', None)
        if limit:
            try:
                queryset = queryset[:int(limit)]
            except ValueError:
                pass
        
        return queryset


class EncryptionHistoryDetailView(generics.RetrieveAPIView):
    """Retrieve a specific encryption history entry."""
    serializer_class = EncryptionHistorySerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        return EncryptionHistory.objects.filter(user=self.request.user)
