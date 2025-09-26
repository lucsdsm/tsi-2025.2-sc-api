from rest_framework import serializers
from .models import Movimentacao, Correntista

class CorrentistaSerializer(serializers.ModelSerializer): # Serializer para o modelo Correntista
    class Meta:
        model = Correntista
        fields = ['id', 'nome_correntista']

class MovimentacaoSerializer(serializers.ModelSerializer):

    correntista = CorrentistaSerializer(read_only=True) # Serializa o correntista associado
    
    correntista_beneficiario = CorrentistaSerializer(read_only=True, allow_null=True) # Serializa o beneficiário, se houver
    
    tipo_operacao_display = serializers.CharField(source='get_tipo_operacao_display', read_only=True) # Campo extra para mostrar 'Crédito' ou 'Débito' de forma amigável

    class Meta:
        model = Movimentacao
        fields = [
            'id', 
            'tipo_operacao_display',
            'valor_operacao', 
            'data_operacao', 
            'descricao', 
            'correntista', 
            'correntista_beneficiario'
        ]