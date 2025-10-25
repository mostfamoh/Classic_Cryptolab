from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import AttackLog
from .serializers import (
    AttackLogSerializer,
    CaesarBruteForceSerializer,
    FrequencyAnalysisSerializer,
    HillKnownPlaintextSerializer,
    AttackRecommendationsSerializer
)
from .attack_algorithms import (
    CaesarBruteForce,
    FrequencyAnalysis,
    HillKnownPlaintextAttack,
    AttackRecommendations
)


class CaesarBruteForceView(APIView):
    """Perform brute force attack on Caesar cipher."""
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request):
        serializer = CaesarBruteForceSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        ciphertext = serializer.validated_data['ciphertext']
        log_attack = serializer.validated_data.get('log_attack', True)
        
        try:
            results = CaesarBruteForce.attack(ciphertext)
            
            # Log the attack
            if log_attack:
                AttackLog.objects.create(
                    user=request.user,
                    cipher_type='caesar',
                    attack_type='brute_force',
                    target_text=ciphertext,
                    results={'attempts': results[:5]},  # Store top 5 results
                    success=True
                )
            
            return Response({
                'success': True,
                'results': results,
                'best_match': results[0] if results else None,
                'total_attempts': len(results)
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class FrequencyAnalysisView(APIView):
    """Perform frequency analysis on text."""
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request):
        serializer = FrequencyAnalysisSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        text = serializer.validated_data['text']
        log_attack = serializer.validated_data.get('log_attack', True)
        
        try:
            results = FrequencyAnalysis.analyze(text)
            
            # Log the attack
            if log_attack:
                AttackLog.objects.create(
                    user=request.user,
                    cipher_type='unknown',
                    attack_type='frequency_analysis',
                    target_text=text,
                    results=results,
                    success=True
                )
            
            return Response({
                'success': True,
                'analysis': results
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class HillKnownPlaintextView(APIView):
    """Perform known-plaintext attack on Hill cipher."""
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request):
        serializer = HillKnownPlaintextSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        plaintext = serializer.validated_data['plaintext']
        ciphertext = serializer.validated_data['ciphertext']
        log_attack = serializer.validated_data.get('log_attack', True)
        
        try:
            results = HillKnownPlaintextAttack.attack(plaintext, ciphertext)
            
            # Log the attack
            if log_attack:
                AttackLog.objects.create(
                    user=request.user,
                    cipher_type='hill',
                    attack_type='known_plaintext',
                    target_text=f"Plain: {plaintext}, Cipher: {ciphertext}",
                    results=results,
                    success=results.get('success', False)
                )
            
            return Response(results, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AttackRecommendationsView(APIView):
    """Get attack recommendations for a cipher type."""
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request):
        serializer = AttackRecommendationsSerializer(data=request.query_params)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        cipher_type = serializer.validated_data['cipher_type']
        recommendations = AttackRecommendations.get_recommendations(cipher_type)
        
        return Response(recommendations, status=status.HTTP_200_OK)


class AttackLogListView(generics.ListAPIView):
    """List attack logs for the current user."""
    serializer_class = AttackLogSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        queryset = AttackLog.objects.filter(user=self.request.user)
        
        # Filter by cipher type
        cipher_type = self.request.query_params.get('cipher_type', None)
        if cipher_type:
            queryset = queryset.filter(cipher_type=cipher_type)
        
        # Filter by attack type
        attack_type = self.request.query_params.get('attack_type', None)
        if attack_type:
            queryset = queryset.filter(attack_type=attack_type)
        
        return queryset


class AttackLogDetailView(generics.RetrieveAPIView):
    """Retrieve a specific attack log."""
    serializer_class = AttackLogSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        return AttackLog.objects.filter(user=self.request.user)
